from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import DirectoryTree, Static, Button, TextArea, Input, Label
from textual.binding import Binding
from ...ui.mixins.focus_mixin import InitialFocusMixin
import time
from typing import Optional
from textual.message import Message
from rich.syntax import Syntax
from rich.text import Text
from rich.markup import escape
import os
from textual.coordinate import Coordinate
from textual.widgets import DataTable
from jedi import Script
from difflib import SequenceMatcher
import re


class EditorTab:
    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content
        self.modified = False


class FileCreated(Message):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path


class FilterableDirectoryTree(DirectoryTree):
    def __init__(self, path: str, show_hidden: bool = False) -> None:
        super().__init__(path)
        self.show_hidden = show_hidden

    def filter_paths(self, paths: list[str]) -> list[str]:
        if self.show_hidden:
            return paths
        return [path for path in paths if not os.path.basename(path).startswith(".")]

    def refresh_tree(self) -> None:
        self.path = self.path
        self.reload()
        self.refresh(layout=True)


class NewFileDialog(ModalScreen):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("f1", "submit", "Submit"),
        Binding("tab", "next_field", "Next Field"),
    ]

    def __init__(self, initial_path: str) -> None:
        super().__init__()
        self.selected_path = initial_path

    def compose(self) -> ComposeResult:
        with Container(classes="file-form-container"):
            with Vertical(classes="file-form"):
                yield Static("Create New File", classes="file-form-header")

                with Vertical():
                    yield Label("Selected Directory:", classes="selected-path-label")
                    yield Static(str(self.selected_path), id="selected-path")

                with Vertical():
                    yield Label("Filename")
                    yield Input(placeholder="Enter filename", id="filename")

                yield FilterableDirectoryTree(os.path.expanduser("~"))

                with Horizontal(classes="form-buttons"):
                    yield Button("Cancel", variant="error", id="cancel")
                    yield Button("Create File", variant="success", id="submit")

    def on_mount(self) -> None:
        self.query_one("#filename").focus()

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        self.selected_path = event.path
        self.query_one("#selected-path").update(str(self.selected_path))

    def on_input_submitted(self) -> None:
        self.action_submit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "submit":
            self._handle_submit()

    def _handle_submit(self) -> None:
        filename = self.query_one("#filename").value
        if not filename:
            self.notify("Filename is required", severity="error")
            return

        full_path = os.path.join(self.selected_path, filename)

        if os.path.exists(full_path):
            self.notify("File already exists!", severity="error")
            return

        try:
            with open(full_path, "w") as f:
                f.write("")
            self.dismiss(full_path)
            self.app.post_message(FileCreated(full_path))
            tree = self.app.query_one(FilterableDirectoryTree)
            tree.refresh_tree()
            editor = self.app.query_one(CodeEditor)
            # open the file as soon as it's created
            editor.open_file(full_path)
            editor.focus()
            self.dismiss(full_path)
        except Exception as e:
            self.notify(f"Error creating file: {str(e)}", severity="error")
            self.dismiss(None)

    async def action_cancel(self) -> None:
        self.dismiss(None)

    async def action_submit(self) -> None:
        self._handle_submit()

    async def action_next_field(self) -> None:
        current = self.app.focused
        if isinstance(current, Input):
            self.query_one(FilterableDirectoryTree).focus()
        elif isinstance(current, FilterableDirectoryTree):
            self.query_one("#submit").focus()
        elif isinstance(current, Button):
            self.query_one("#filename").focus()
        else:
            self.query_one("#filename").focus()


class StatusBar(Static):
    def __init__(self) -> None:
        super().__init__("", id="status-bar")
        self.mode = "NORMAL"
        self.file_info = ""
        self.command = ""
        self._update_content()

    def update_mode(self, mode: str) -> None:
        self.mode = mode.upper()
        self._update_content()

    def update_file_info(self, info: str) -> None:
        self.file_info = info
        self._update_content()

    def update_command(self, command: str) -> None:
        self.command = command
        self._update_content()

    def _update_content(self) -> None:
        # Example: color the mode, but escape dynamic text so it doesn’t break markup
        mode_style = {"NORMAL": "cyan", "INSERT": "green", "COMMAND": "yellow"}
        color = mode_style.get(self.mode, "white")

        # Build markup parts
        parts = [f"[{color}]{self.mode}[/]"]
        if self.file_info:
            parts.append(escape(self.file_info))
        if self.command:
            parts.append(f"[yellow]{escape(self.command)}[/]")

        # Turn the combined markup string into a Rich Text object
        text = Text.from_markup(" ".join(parts))

        # Update the StatusBar with Rich Text (no markup=... argument needed)
        self.update(text)


class AutoCompletePopup(DataTable):
    """Popup widget for displaying autocompletion suggestions."""

    class Selected(Message):
        """Message emitted when a completion is selected."""

        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def __init__(self) -> None:
        super().__init__()
        self.cursor_type = "row"
        self.add_column("Completion", width=30)
        self.add_column("Type", width=20)
        self.add_column("Info", width=40)
        self.styles.background = "rgb(30,30,30)"
        self.styles.width = 90
        self.styles.height = 10
        self.can_focus = True

        self.styles.row_hover = "rgb(50,50,50)"
        self.styles.row_selected = "rgb(60,60,100)"
        self.styles.row_cursor = "rgb(70,70,120)"

    def on_mount(self) -> None:
        self.cursor_type = "row"
        # Select first row by default if there are rows
        if self.row_count > 0:
            self.move_cursor(row=0, column=0)

    def populate(self, completions: list) -> None:
        self.clear()
        for completion in completions:
            name = completion.name
            type_ = completion.type
            info = completion.description or ""

            type_indicators = {
                "function": "🔧",
                "class": "📦",
                "module": "📚",
                "keyword": "🔑",
                "builtin": "⚡",
                "local": "📎",
                "method": "⚙️",
                "property": "🔹",
            }
            type_icon = type_indicators.get(type_, "•")

            self.add_row(f"{type_icon} {name}", type_, info)

        if self.row_count > 0:
            self.move_cursor(row=0, column=0)

    def on_key(self, event) -> None:
        if event.key == "enter" or event.key == "tab":
            if self.cursor_row is not None:
                value = self.get_cell_at(Coordinate(self.cursor_row, 0))
                # Strip the type icon from the value
                value = value.split(" ", 1)[1] if " " in value else value
                self.post_message(self.Selected(value))
            event.prevent_default()
            event.stop()
        elif event.key == "escape":
            self.post_message(self.Selected(""))
            event.prevent_default()
            event.stop()
        elif event.key == "up":
            if self.cursor_row is not None and self.cursor_row > 0:
                self.move_cursor(row=self.cursor_row - 1, column=0)
            event.prevent_default()
            event.stop()
        elif event.key == "down":
            if self.cursor_row is not None and self.cursor_row < self.row_count - 1:
                self.move_cursor(row=self.cursor_row + 1, column=0)
            event.prevent_default()
            event.stop()


class CodeEditor(TextArea):

    class _LocalCompletion:
        def __init__(self, name: str):
            self.name = name
            self.type = "local"
            self.description = f"Local symbol: {name}"
            self.score = 0

    def _get_local_completions(self) -> list:

        # Basic pattern for Python identifiers (variable/function/class names, etc.)
        pattern = re.compile(r"[A-Za-z_]\w*")
        tokens_found = set(pattern.findall(self.text))
        python_keywords = {
            "False",
            "None",
            "True",
            "and",
            "as",
            "assert",
            "async",
            "await",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "nonlocal",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
        }
        tokens_found = tokens_found - python_keywords

        # Convert each found token into a _LocalCompletion object
        local_completions = []
        for tok in sorted(tokens_found):
            # You might skip single-letter tokens or do more filtering:
            # if len(tok) == 1:
            #     continue
            local_completions.append(CodeEditor._LocalCompletion(tok))

        return local_completions

    BINDINGS = [
        Binding("ctrl+n", "new_file", "New File", show=True),
        Binding("tab", "indent", "Indent", show=False),
        Binding("shift+tab", "unindent", "Unindent", show=False),
        Binding("ctrl+]", "indent", "Indent", show=False),
        Binding("ctrl+[", "unindent", "Unindent", show=False),
        Binding("ctrl+s", "save_file", "Save File", show=True),
        Binding("escape", "enter_normal_mode", "Enter Normal Mode", show=False),
        Binding("i", "enter_insert_mode", "Enter Insert Mode", show=False),
        Binding("h", "move_left", "Move Left", show=False),
        Binding("l", "move_right", "Move Right", show=False),
        Binding("j", "move_down", "Move Down", show=False),
        Binding("k", "move_up", "Move Up", show=False),
        Binding("w", "move_word_forward", "Move Word Forward", show=False),
        Binding("b", "move_word_backward", "Move Word Backward", show=False),
        Binding("0", "move_line_start", "Move to Line Start", show=False),
        Binding("$", "move_line_end", "Move to Line End", show=False),
        Binding("shift+left", "focus_tree", "Focus Tree", show=True),
        Binding("u", "undo", "Undo", show=False),
        Binding("ctrl+r", "redo", "Redo", show=False),
        Binding(":w", "write", "Write", show=False),
        Binding(":wq", "write_quit", "Write and Quit", show=False),
        Binding(":q", "quit", "Quit", show=False),
        Binding(":q!", "force_quit", "Force Quit", show=False),
        Binding("%d", "clear_editor", "Clear Editor", show=False),
        Binding("ctrl+z", "noop", ""),
        Binding("ctrl+y", "noop", ""),
        Binding("ctrl+space", "show_completions", "Show Completions", show=True),
    ]

    class FileModified(Message):
        def __init__(self, is_modified: bool) -> None:
            super().__init__()
            self.is_modified = is_modified

        def action_noop(self) -> None:
            pass

    def __init__(self) -> None:
        super().__init__(language="python", theme="monokai", show_line_numbers=True)
        self.current_file = None
        self._modified = False
        self.tab_size = 4
        self._syntax = None
        self.language = None
        self.highlight_text = None
        self.mode = "insert"
        self._undo_stack = []
        self._redo_stack = []
        self._last_text = ""
        self._is_undoing = False
        self.command = ""
        self.in_command_mode = False
        self.pending_command = ""
        self.status_bar = StatusBar()
        self.status_bar.update_mode("NORMAL")
        self.tabs = []
        self.active_tab_index = -1
        self._last_scroll_position = (0, 0)
        self._last_cursor_position = (0, 0)
        self.autopairs = {"{": "}", "(": ")", "[": "]", '"': '"', "'": "'"}
        self._last_action_time = time.time()
        self._undo_batch = []
        self._batch_timeout = (
            0.3  # we can mess around with this for more or less granular state saving
        )
        self._completion_popup = None
        self._word_pattern = re.compile(r"[\w\.]")

        # Add new attributes for smarter completion
        self._builtins = {
            "print": ("function", "Print objects to the text stream"),
            "len": ("function", "Return the length of an object"),
            "str": ("function", "Return a string version of an object"),
            "int": ("function", "Convert a number or string to an integer"),
            "list": ("function", "Create a new list"),
            "dict": ("function", "Create a new dictionary"),
            "range": ("function", "Create a sequence of numbers"),
            "open": ("function", "Open a file"),
            "type": ("function", "Return the type of an object"),
            # Add more common builtins
        }

        self._common_patterns = {
            "if ": ("keyword", "Start an if statement"),
            "for ": ("keyword", "Start a for loop"),
            "while ": ("keyword", "Start a while loop"),
            "def ": ("keyword", "Define a function"),
            "class ": ("keyword", "Define a class"),
            "import ": ("keyword", "Import a module"),
            "from ": ("keyword", "Import specific names from a module"),
            "return ": ("keyword", "Return from a function"),
            "try": ("keyword", "Start a try-except block"),
            "with ": ("keyword", "Context manager statement"),
        }

        self._common_imports = {
            "os": "Operating system interface",
            "sys": "System-specific parameters and functions",
            "json": "JSON encoder and decoder",
            "datetime": "Basic date and time types",
            "random": "Generate random numbers",
            "math": "Mathematical functions",
            "pathlib": "Object-oriented filesystem paths",
            "typing": "Support for type hints",
            "collections": "Container datatypes",
            "re": "Regular expression operations",
        }

    def _save_positions(self) -> None:
        self._last_scroll_position = self.scroll_offset
        self._last_cursor_position = self.cursor_location

    def _restore_positions(self) -> None:
        self.scroll_to(self._last_scroll_position[0], self._last_scroll_position[1])
        self.move_cursor(self._last_cursor_position)

    """def on_focus(self) -> None:
        current_scroll = self.scroll_offset
        super().on_focus()
        self.scroll_to(current_scroll[0], current_scroll[1], animate=False)"""

    def compose(self) -> ComposeResult:
        yield self.status_bar

    def on_mount(self) -> None:
        self.status_bar.update_mode("NORMAL")
        self._update_status_info()

    def _update_status_info(self) -> None:
        file_info = []
        if self.tabs:
            file_info.append(f"[{self.active_tab_index + 1}/{len(self.tabs)}]")
        if self.current_file:
            file_info.append(os.path.basename(self.current_file))
        if self._modified:
            file_info.append("[red][+][/]")
        if self.text:
            lines = len(self.text.split("\n"))
            chars = len(self.text)
            file_info.append(f"{lines}L, {chars}B")

        self.status_bar.update_file_info(" ".join(file_info))

    def get_current_indent(self) -> str:
        lines = self.text.split("\n")
        if not lines:
            return ""
        current_line = lines[self.cursor_location[0]]
        indent = ""
        for char in current_line:
            if char.isspace():
                indent += char
            else:
                break
        return indent

    def should_increase_indent(self) -> bool:
        lines = self.text.split("\n")
        if not lines:
            return False
        current_line = lines[self.cursor_location[0]]
        stripped_line = current_line.strip()

        if stripped_line.endswith(":"):
            return True

        brackets = {"(": ")", "[": "]", "{": "}"}
        counts = {
            k: stripped_line.count(k) - stripped_line.count(v)
            for k, v in brackets.items()
        }
        return any(count > 0 for count in counts.values())

    def should_decrease_indent(self) -> bool:
        lines = self.text.split("\n")
        if not lines or self.cursor_location[0] == 0:
            return False

        current_line = lines[self.cursor_location[0]]
        stripped_line = current_line.strip()

        if stripped_line.startswith((")", "]", "}")):
            return True

        dedent_keywords = {"return", "break", "continue", "pass", "raise"}
        first_word = stripped_line.split()[0] if stripped_line else ""
        return first_word in dedent_keywords

    def handle_indent(self) -> None:
        current_indent = self.get_current_indent()
        lines = self.text.split("\n")
        current_line = lines[self.cursor_location[0]] if lines else ""
        cursor_col = self.cursor_location[1]

        # Check if cursor is between brackets
        if cursor_col > 0 and cursor_col < len(current_line):
            prev_char = current_line[cursor_col - 1]
            next_char = current_line[cursor_col]
            bracket_pairs = {"{": "}", "(": ")", "[": "]"}

            # If we're between matching brackets
            if prev_char in bracket_pairs and next_char == bracket_pairs[prev_char]:
                # Insert two newlines and position cursor in between
                indent_level = current_indent + " " * self.tab_size
                self.insert(f"\n{indent_level}\n{current_indent}")
                # Move cursor up one line and to end of indent
                self.move_cursor((self.cursor_location[0] - 1, len(indent_level)))
                return

        if not current_indent and not self.text:
            self.insert("\n")
            return

        if self.should_decrease_indent():
            new_indent = (
                current_indent[: -self.tab_size]
                if len(current_indent) >= self.tab_size
                else ""
            )
            self.insert("\n" + new_indent)
        elif self.should_increase_indent():
            self.insert("\n" + current_indent + " " * self.tab_size)
        else:
            self.insert("\n" + current_indent)

    def handle_backspace(self) -> None:
        if not self.text:
            return

        cur_row, cur_col = self.cursor_location
        lines = self.text.split("\n")
        if cur_row >= len(lines):
            return

        current_line = lines[cur_row]

        # Check for empty bracket pairs
        if cur_col >= 1 and cur_col < len(current_line) + 1:
            prev_char = current_line[cur_col - 1]
            if prev_char in self.autopairs:
                if (
                    cur_col < len(current_line)
                    and current_line[cur_col] == self.autopairs[prev_char]
                ):
                    current_scroll = self.scroll_offset
                    lines[cur_row] = (
                        current_line[: cur_col - 1] + current_line[cur_col + 1 :]
                    )
                    self.text = "\n".join(lines)
                    self.move_cursor((cur_row, cur_col - 1))
                    self.scroll_to(current_scroll[0], current_scroll[1], animate=False)
                    return

        if cur_col == 0 and cur_row > 0:
            self.action_delete_left()
            return

        prefix = current_line[:cur_col]
        if prefix.isspace():
            spaces_to_delete = min(self.tab_size, len(prefix.rstrip()) or len(prefix))
            for _ in range(spaces_to_delete):
                self.action_delete_left()
        else:
            self.action_delete_left()

    def on_key(self, event) -> None:
        # Handle tab key specially for completions
        if event.key == "tab" and self.mode == "insert":
            if self._completion_popup and self._completion_popup.row_count > 0:
                # Get the currently selected completion.
                selected_row = self._completion_popup.cursor_row or 0
                value = self._completion_popup.get_cell_at(Coordinate(selected_row, 0))
                # Strip the type icon.
                value = value.split(" ", 1)[1] if " " in value else value

                # **Save the current scroll offset before updating text**
                current_scroll = self.scroll_offset

                # Apply the completion.
                lines = self.text.split("\n")
                row, col = self.cursor_location
                current_word, word_start = self._get_current_word()
                line = lines[row]
                lines[row] = line[:word_start] + value + line[col:]
                self.text = "\n".join(lines)
                self.move_cursor((row, word_start + len(value)))

                # **Restore the scroll offset after updating the text**
                self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

                # Hide popup.
                self.hide_completions()
                event.prevent_default()
                event.stop()
                return
            else:
                # Normal tab behavior.
                self.action_indent()
                event.prevent_default()
                event.stop()
                return

        if (
            self.mode == "insert"
            and self._completion_popup
            and event.key in ["up", "down"]
        ):
            self._completion_popup.focus()
            event.prevent_default()
            event.stop()
            return

        if (
            self.mode == "insert"
            and self._completion_popup
            and event.key in ["left", "right"]
        ):
            self.hide_completions()

        # Handle completion popup
        if self._completion_popup:
            if event.key == "escape":
                self.hide_completions()
                if self.mode == "insert":
                    # Don't switch to normal mode when dismissing completion
                    event.prevent_default()
                    event.stop()
                return
            elif event.key == "enter":
                return

        if (
            self.mode == "insert"
            and event.is_printable
            and self._word_pattern.match(event.character)
        ):
            # If the popup already exists, update it with new completions.
            if self._completion_popup:
                completions = self._get_completions()
                if completions:
                    self._completion_popup.populate(completions)
                else:
                    self.hide_completions()
            else:
                # Create and mount the popup if it doesn’t exist yet.
                completions = self._get_completions()
                if completions:
                    row, col = self.cursor_location
                    popup = AutoCompletePopup()
                    popup.populate(completions)
                    popup.styles.offset = (col, row + 1)
                    self._completion_popup = popup
                    self.mount(popup)

        elif (
            self.mode == "insert"
            and event.is_printable
            and not self._word_pattern.match(event.character)
        ):
            # Hide the autocomplete popup if the typed character isn't part of a valid word.
            self.hide_completions()

        if self.in_command_mode:
            if event.key == "enter":
                self.execute_command()
                self.in_command_mode = False
                self.command = ""
                self.refresh()
                event.prevent_default()
                event.stop()
            elif event.key == "escape":
                self.in_command_mode = False
                self.command = ""
                self.refresh()
                event.prevent_default()
                event.stop()
            elif event.is_printable:
                self.command += event.character
                self.refresh()
                event.prevent_default()
                event.stop()
            elif event.key == "backspace":
                self._save_undo_state()
                self.handle_backspace()
                self._modified = True
                self.post_message(self.FileModified(True))
                event.prevent_default()
                event.stop()
            self.status_bar.update_mode("COMMAND")
            self.status_bar.update_command(self.command)
        else:
            if self.mode == "insert":
                if event.key == "enter":
                    self.cursor_type = "line"
                    self._save_undo_state()
                    self.handle_indent()
                    self._modified = True
                    self.post_message(self.FileModified(True))
                    event.prevent_default()
                    event.stop()
                elif event.is_printable:
                    self.cursor_type = "line"
                    self._save_undo_state()
                    if event.character in self.autopairs:
                        cur_pos = self.cursor_location
                        self.insert(event.character + self.autopairs[event.character])
                        self.move_cursor((cur_pos[0], cur_pos[1] + 1))

                    else:
                        self.insert(event.character)
                    self._modified = True
                    self.post_message(self.FileModified(True))
                    event.prevent_default()
                    event.stop()
                elif event.key == "backspace":
                    self._save_undo_state()
                    self.handle_backspace()
                    self._modified = True
                    self.post_message(self.FileModified(True))
                    event.prevent_default()
                    event.stop()
                elif event.key in ["left", "right", "up", "down"]:
                    return
            elif self.mode == "normal":
                if event.key == "backspace":
                    self._save_undo_state()
                    self.handle_backspace()
                    self._modified = True
                    self.post_message(self.FileModified(True))
                    event.prevent_default()
                    event.stop()
                elif event.key == "u":
                    self.action_undo()
                    event.prevent_default()
                    event.stop()
                elif event.key == "ctrl+r":
                    self.action_redo()
                    event.prevent_default()
                    event.stop()
                motion_map = {
                    "h": self.action_move_left,
                    "l": self.action_move_right,
                    "j": self.action_move_down,
                    "k": self.action_move_up,
                    "w": self.action_move_word_forward,
                    "b": self.action_move_word_backward,
                    "0": self.action_move_line_start,
                    "$": self.action_move_line_end,
                    "x": self.action_delete_char,
                    "dd": self.action_delete_line,
                    "de": self.action_delete_to_end,
                }

                if self.pending_command and event.character:
                    combined_command = self.pending_command + event.character
                    if combined_command in motion_map:
                        motion_map[combined_command]()
                        self.pending_command = ""
                    else:
                        self.pending_command = ""
                    event.prevent_default()
                    event.stop()
                elif event.character == "d":
                    self.pending_command = "d"
                    event.prevent_default()
                    event.stop()
                elif event.character in motion_map:
                    motion_map[event.character]()
                    event.prevent_default()
                    event.stop()
                elif event.character == "i":
                    self.mode = "insert"
                    self.status_bar.update_mode("INSERT")
                    self.cursor_blink = True
                    event.prevent_default()
                    event.stop()
                elif event.character == ":":
                    self.in_command_mode = True
                    self.command = ":"
                    self.refresh()
                    event.prevent_default()
                    event.stop()
                elif event.key in ["left", "right", "up", "down"]:
                    return
                else:
                    if event.is_printable:
                        event.prevent_default()
                        event.stop()

    def _get_current_word(self) -> tuple[str, int]:
        row, col = self.cursor_location
        if not self.text:
            return "", col

        lines = self.text.split("\n")
        if row >= len(lines):
            return "", col

        line = lines[row]
        if not line:
            return "", col

        word_start = col
        while word_start > 0 and re.match(r"\w", line[word_start - 1]):
            word_start -= 1

        # If there's a dot in the part preceding the current word, only complete the part after the last dot.
        # This should be extended to handle more complex cases (like nested attributes).
        last_dot = line.rfind(".", word_start, col)
        if last_dot != -1:
            word_start = last_dot + 1

        current_word = line[word_start:col]
        return current_word, word_start

    def _get_completions(self) -> list:
        try:
            current_word, _ = self._get_current_word()
            suggestions = []
            seen = set()

            for name, (type_, desc) in self._builtins.items():
                if name.startswith(current_word):
                    comp = self._create_completion(name, "builtin", desc)
                    comp.score = 1000
                    suggestions.append(comp)
                    seen.add(name)

            context_suggestions = self._get_context_suggestions()
            for suggestion in context_suggestions:
                if suggestion.name not in seen and suggestion.name.startswith(
                    current_word
                ):
                    suggestion.score = 800
                    suggestions.append(suggestion)
                    seen.add(suggestion.name)

            if self.current_file:
                try:
                    script = Script(code=self.text, path=self.current_file)
                    row, column = self.cursor_location
                    jedi_completions = script.complete(row + 1, column)
                    for comp in jedi_completions:
                        if comp.name not in seen:
                            comp.score = 500
                            suggestions.append(comp)
                            seen.add(comp.name)
                except Exception:
                    pass

            local_completions = self._get_local_completions()
            for comp in local_completions:
                if comp.name not in seen:
                    comp.score = 100
                    suggestions.append(comp)
                    seen.add(comp.name)

            return sorted(
                suggestions, key=lambda x: (-getattr(x, "score", 0), x.name.lower())
            )

        except Exception as e:
            self.notify(f"Completion error: {str(e)}", severity="error")
            return []

    def _score_suggestion(self, suggestion, current_word: str) -> float:
        name = suggestion.name.lower()
        current = current_word.lower()

        similarity = SequenceMatcher(None, current, name).ratio()
        score = similarity * 100

        if name.startswith(current):
            score += 20

        score += 1.0 / len(name)

        type_bonus = {
            "function": 2.0,
            "class": 2.0,
            "keyword": 3.0,
            "module": 1.5,
            "method": 1.5,
            "property": 1.0,
        }
        score += type_bonus.get(getattr(suggestion, "type", ""), 0.0)

        return score

    def _fuzzy_match(self, pattern: str, text: str) -> bool:
        """Simple fuzzy matching algorithm"""
        pattern = pattern.lower()
        text = text.lower()

        if not pattern or not text:
            return False

        pattern_idx = 0
        for char in text:
            if char == pattern[pattern_idx]:
                pattern_idx += 1
                if pattern_idx == len(pattern):
                    return True
        return False

    def _get_context_suggestions(self) -> list:
        row, col = self.cursor_location
        lines = self.text.split("\n")
        current_line = lines[row] if row < len(lines) else ""
        line_before_cursor = current_line[:col]

        suggestions = []

        current_word, _ = self._get_current_word()
        if current_word.startswith("@"):
            decorators = [
                ("@classmethod", "decorator", "Class method decorator"),
                ("@staticmethod", "decorator", "Static method decorator"),
                ("@property", "decorator", "Property decorator"),
                # More common decorators should be added here
            ]
            for name, type_, desc in decorators:
                suggestions.append(self._create_completion(name, type_, desc))
            return suggestions

        if line_before_cursor.strip().startswith(("import", "from")):
            for module, desc in self._common_imports.items():
                suggestions.append(self._create_completion(module, "module", desc))
            return suggestions

        if line_before_cursor.strip() == "":
            for pattern, (type_, desc) in self._common_patterns.items():
                suggestions.append(self._create_completion(pattern, type_, desc))

        for name, (type_, desc) in self._builtins.items():
            suggestions.append(self._create_completion(name, type_, desc))

        return suggestions

    def _create_completion(
        self, name: str, type_: str, description: str
    ) -> "_LocalCompletion":
        completion = self._LocalCompletion(name)
        completion.type = type_
        completion.description = description
        return completion

    def action_show_completions(self) -> None:
        completions = self._get_completions()
        if not completions:
            return

        popup = AutoCompletePopup()
        popup.populate(completions)

        row, col = self.cursor_location
        popup.styles.offset = (col, row + 1)

        self._completion_popup = popup
        self.mount(popup)

        popup.focus()

    def hide_completions(self) -> None:
        if self._completion_popup:
            self._completion_popup.remove()
            self._completion_popup = None

    def on_auto_complete_popup_selected(
        self, message: AutoCompletePopup.Selected
    ) -> None:
        current_scroll = self.scroll_offset

        if message.value:
            lines = self.text.split("\n")
            row, col = self.cursor_location
            current_word, word_start = self._get_current_word()
            line = lines[row]
            lines[row] = line[:word_start] + message.value + line[col:]
            self.text = "\n".join(lines)
            new_cursor_col = word_start + len(message.value)
            self.move_cursor((row, new_cursor_col))

        self.hide_completions()

        self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

        self.focus()
        self.mode = "insert"
        self.status_bar.update_mode("INSERT")
        self.cursor_blink = True

    def execute_command(self) -> None:
        command = self.command[1:].strip()

        if command == "w":
            self.action_write()
            self.status_bar.update_mode("NORMAL")
            self.in_command_mode = False
            self.command = ""
            self.refresh()
        elif command == "wq":
            if not self.current_file:
                self.notify("No file name", severity="error")
                return
            self.action_save_file()
            if self.tabs:
                self.close_current_tab()
            else:
                self.clear_editor()
        elif command == "q":
            if self._modified:
                self.notify(
                    "No write since last change (add ! to override)", severity="warning"
                )
                self.status_bar.update_mode("NORMAL")
                self.in_command_mode = False
                self.command = ""
                self.refresh()
                return

            if self.tabs:
                self.close_current_tab()
            else:
                self.clear_editor()
        elif command == "q!":
            if self.tabs:
                self.close_current_tab()
            else:
                self.clear_editor()
        elif command == "%d":
            self.clear_editor()
        elif command == "n" or command == "bn":
            if self.tabs:
                self.active_tab_index = (self.active_tab_index + 1) % len(self.tabs)
                tab = self.tabs[self.active_tab_index]
                self.load_text(tab.content)
                self.current_file = tab.path
                self.set_language_from_file(
                    tab.path
                )  # update language to match each buffer respectively
                self._update_status_info()
        elif command == "p" or command == "bp":
            if self.tabs:
                self.active_tab_index = (self.active_tab_index - 1) % len(self.tabs)
                tab = self.tabs[self.active_tab_index]
                self.load_text(tab.content)
                self.current_file = tab.path
                self.set_language_from_file(tab.path)  # same here
                self._update_status_info()
        elif command == "ls":
            buffer_list = []
            for i, tab in enumerate(self.tabs):
                marker = "%" if i == self.active_tab_index else " "
                modified = "+" if tab.modified else " "
                name = os.path.basename(tab.path)
                buffer_list.append(f"{i + 1}{marker}{modified} {name}")
            self.notify("\n".join(buffer_list))
        else:
            self.notify(f"Unknown command: {command}", severity="warning")

    def close_current_tab(self) -> None:
        if not self.tabs:
            return

        self.tabs.pop(self.active_tab_index)
        if self.tabs:
            self.active_tab_index = max(
                0, min(self.active_tab_index, len(self.tabs) - 1)
            )
            tab = self.tabs[self.active_tab_index]
            self.load_text(tab.content)
            self.current_file = tab.path
        else:
            self.active_tab_index = -1
            self.load_text("")
            self.current_file = None
        self._update_status_info()

    def render(self) -> str:
        content = str(super().render())

        if self.in_command_mode:
            content += f"\nCommand: {self.command}"

        return content

    def set_language_from_file(self, filepath: str) -> None:
        ext = os.path.splitext(filepath)[1].lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".html": "html",
            ".css": "css",
            ".md": "markdown",
            ".json": "json",
            ".sh": "bash",
            ".sql": "sql",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".xml": "xml",
            ".txt": None,
        }

        self.language = language_map.get(ext)
        if self.language:
            try:
                self._syntax = Syntax(
                    self.text,
                    self.language,
                    theme="monokai",
                    line_numbers=True,
                    word_wrap=False,
                    indent_guides=True,
                )
                self.update_syntax_highlighting()
            except Exception as e:
                self.notify(f"Syntax highlighting error: {e}", severity="error")

    def update_syntax_highlighting(self) -> None:
        if self.language and self.text and self._syntax:
            try:
                self._syntax.code = self.text
                rich_text = Text.from_ansi(str(self._syntax))
                self.highlight_text = rich_text
            except (SyntaxError, ValueError) as e:
                self.notify(f"Highlighting update error: {e}", severity="error")

    def clear_editor(self) -> None:
        self.text = ""
        if self.command == "%d":
            self.notify("Editor Cleared", severity="info")
        self.refresh()

    def action_write(self) -> None:
        if not self.current_file:
            self.notify("No file to save", severity="warning")
            return

        self.action_save_file()

    def action_write_quit(self) -> None:
        if not self.current_file:
            self.notify("No file to save", severity="warning")
            return

        self.action_save_file()
        if self.tabs:
            self.close_current_tab()
        else:
            self.clear_editor()

    def action_quit(self) -> None:
        if self._modified:
            self.notify(
                "No write since last change (add ! to override)", severity="warning"
            )
            return

        if self.tabs:
            self.close_current_tab()
        else:
            self.clear_editor()

    def action_force_quit(self) -> None:
        if self.tabs:
            self.close_current_tab()
        else:
            self.clear_editor()

    def action_indent(self) -> None:
        cursor_location = self.cursor_location
        self.insert(" " * self.tab_size)
        new_location = (cursor_location[0], cursor_location[1] + self.tab_size)
        self.move_cursor(new_location)

    def action_unindent(self) -> None:
        cursor_location = self.cursor_location
        lines = self.text.split("\n")
        current_line = lines[cursor_location[0]] if lines else ""

        if current_line.startswith(" " * self.tab_size):
            self.move_cursor((cursor_location[0], 0))
            for _ in range(self.tab_size):
                self.action_delete_left()

    def action_save_file(self) -> None:
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text)
                self._modified = False
                self.post_message(self.FileModified(False))
                saved_size = os.path.getsize(self.current_file)
                self.notify(
                    f"Wrote {saved_size} bytes to {os.path.basename(self.current_file)}"
                )
                self._update_status_info()
            except (IOError, OSError) as e:
                self.notify(f"Error saving file: {e}", severity="error")

    def watch_text(self, old_text: str, new_text: str) -> None:
        if old_text != new_text:
            if not self._is_undoing:
                current_cursor = self.cursor_location
                self._undo_stack.append(old_text)
                self._redo_stack.clear()

            self._modified = True
            self.post_message(self.FileModified(True))

            if self.tabs and self.active_tab_index >= 0:
                self.tabs[self.active_tab_index].content = new_text
                self.tabs[self.active_tab_index].modified = True

            if self._syntax:
                self.update_syntax_highlighting()
            self._update_status_info()

    def action_enter_normal_mode(self) -> None:
        self.mode = "normal"
        self.status_bar.update_mode("NORMAL")
        self.cursor_blink = False

    def action_enter_insert_mode(self) -> None:
        self.mode = "insert"
        self.status_bar.update_mode("INSERT")
        self.cursor_blink = True
        self.cursor_style = "underline"

    def action_move_left(self) -> None:
        if self.mode == "normal":
            self.move_cursor_relative(-1, 0)

    def action_move_right(self) -> None:
        if self.mode == "normal":
            self.move_cursor_relative(1, 0)

    def action_move_down(self) -> None:
        if self.mode == "normal":
            self.move_cursor_relative(0, 1)

    def action_move_up(self) -> None:
        if self.mode == "normal":
            self.move_cursor_relative(0, -1)

    def action_move_word_forward(self) -> None:
        if self.mode == "normal":
            current_scroll = self.scroll_offset
            lines = self.text.split("\n")
            cur_row, cur_col = self.cursor_location
            line = lines[cur_row] if cur_row < len(lines) else ""
            while cur_col < len(line) and line[cur_col].isspace():
                cur_col += 1
            while cur_col < len(line) and not line[cur_col].isspace():
                cur_col += 1
            self.move_cursor((cur_row, cur_col))
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_move_word_backward(self) -> None:
        if self.mode == "normal":
            current_scroll = self.scroll_offset
            lines = self.text.split("\n")
            cur_row, cur_col = self.cursor_location
            line = lines[cur_row] if cur_row < len(lines) else ""
            while cur_col > 0 and line[cur_col - 1].isspace():
                cur_col -= 1
            while cur_col > 0 and not line[cur_col - 1].isspace():
                cur_col -= 1
            self.move_cursor((cur_row, cur_col))
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_move_line_start(self) -> None:
        if self.mode == "normal":
            current_scroll = self.scroll_offset
            self.move_cursor((self.cursor_location[0], 0))
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_undo(self) -> None:
        if self.mode == "normal" and self._undo_stack:
            current_scroll = self.scroll_offset
            self._is_undoing = True
            self._redo_stack.append(self.text)
            self.text = self._undo_stack.pop()
            self._undo_batch = []
            self._is_undoing = False
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_redo(self) -> None:
        if self.mode == "normal" and self._redo_stack:
            current_scroll = self.scroll_offset
            self._is_undoing = True
            self._undo_stack.append(self.text)
            self.text = self._redo_stack.pop()
            self._is_undoing = False
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_delete_char(self) -> None:
        if self.mode == "normal":
            current_scroll = self.scroll_offset
            self._save_undo_state()
            cur_row, cur_col = self.cursor_location
            lines = self.text.split("\n")
            if cur_row < len(lines):
                if cur_col < len(lines[cur_row]):
                    lines[cur_row] = (
                        lines[cur_row][:cur_col] + lines[cur_row][cur_col + 1 :]
                    )
                else:
                    lines[cur_row] = lines[cur_row][:cur_col]
                self.text = "\n".join(lines)
                if cur_col < len(lines[cur_row]):
                    self.move_cursor((cur_row, cur_col))
                else:
                    self.move_cursor((cur_row, max(cur_col - 1, 0)))
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_delete_line(self) -> None:
        if self.mode == "normal":
            self._save_undo_state()
            cur_row, _ = self.cursor_location
            current_scroll = self.scroll_offset
            lines = self.text.split("\n")
            if cur_row < len(lines):
                lines.pop(cur_row)
                self.text = "\n".join(lines)
                target_row = min(cur_row, len(lines) - 1) if lines else 0
                self.move_cursor((target_row, 0))
                self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_delete_to_end(self) -> None:
        if self.mode == "normal":
            current_scroll = self.scroll_offset
            self._save_undo_state()
            cur_row, cur_col = self.cursor_location
            lines = self.text.split("\n")
            if cur_row < len(lines):
                line = lines[cur_row]
                start_col = cur_col
                while cur_col < len(line) and not line[cur_col].isspace():
                    cur_col += 1
                lines[cur_row] = line[:start_col] + line[cur_col:]
                self.text = "\n".join(lines)
                self.move_cursor((cur_row, start_col))
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def action_move_line_end(self) -> None:
        if self.mode == "normal":
            current_scroll = self.scroll_offset
            lines = self.text.split("\n")
            cur_row = self.cursor_location[0]
            if cur_row < len(lines):
                line_length = len(lines[cur_row])
                self.move_cursor((cur_row, line_length))
            self.scroll_to(current_scroll[0], current_scroll[1], animate=False)

    def _save_undo_state(self) -> None:
        if not self._is_undoing:
            current_time = time.time()
            if current_time - self._last_action_time > self._batch_timeout:
                if self._undo_batch:
                    self._undo_stack.append(self._undo_batch[-1])
                    self._undo_batch = []
                self._undo_stack.append(self.text)
                self._redo_stack.clear()
            else:
                self._undo_batch = [self.text]
            self._last_action_time = current_time

    async def action_new_file(self) -> None:
        try:
            tree = self.app.screen.query_one(FilterableDirectoryTree)
            current_path = tree.path if tree.path else os.path.expanduser("~")
        except Exception:
            current_path = os.path.expanduser("~")

        dialog = NewFileDialog(current_path)
        await self.app.push_screen(dialog)

    def open_file(self, filepath: str) -> None:
        try:
            # Check if file is already open in a tab
            for i, tab in enumerate(self.tabs):
                if tab.path == filepath:
                    self.active_tab_index = i
                    self.load_text(tab.content)
                    self.current_file = tab.path
                    self.set_language_from_file(filepath)
                    self._update_status_info()
                    return

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                new_tab = EditorTab(filepath, content)
                self.tabs.append(new_tab)
                self.active_tab_index = len(self.tabs) - 1

                self.load_text(content)
                self.current_file = filepath
                self.set_language_from_file(filepath)
                self._modified = False
                self.mode = "normal"
                self.status_bar.update_mode("NORMAL")
                self.cursor_blink = False
                self.focus()
                self._update_status_info()
        except Exception as e:
            self.notify(f"Error opening file: {str(e)}", severity="error")


class NestView(Container, InitialFocusMixin):
    BINDINGS = [
        Binding("ctrl+h", "toggle_hidden", "Toggle Hidden Files", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+right", "focus_editor", "Focus Editor", show=True),
        Binding("r", "refresh_tree", "Refresh Tree", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.show_hidden = False
        self.show_sidebar = True
        self.editor = None

    async def action_new_file(self) -> None:
        editor = self.query_one(CodeEditor)
        await editor.action_new_file()

    def on_file_created(self, event: FileCreated) -> None:
        self.notify(f"Created file: {os.path.basename(event.path)}")
        tree = self.query_one(FilterableDirectoryTree)
        tree.refresh_tree()

    def compose(self) -> ComposeResult:
        yield Container(
            Horizontal(
                Container(
                    Horizontal(
                        Static("Explorer", classes="nav-title"),
                        Button("-", id="toggle_hidden", classes="toggle-hidden-btn"),
                        Button("New", id="new_file", classes="new-file-btn"),
                        classes="nav-header",
                    ),
                    FilterableDirectoryTree(
                        os.path.expanduser("~"), show_hidden=self.show_hidden
                    ),
                    classes="file-nav",
                ),
                Container(CustomCodeEditor(), classes="editor-container"),
                classes="main-container",
            ),
            id="nest-view",
        )

    def on_mount(self) -> None:
        self.editor = self.query_one(CodeEditor)
        tree = self.query_one(FilterableDirectoryTree)
        tree.focus()

        self.editor.can_focus_tab = True
        self.editor.key_handlers = {
            "ctrl+left": lambda: self.action_focus_tree(),
            "ctrl+n": self.action_new_file,
        }

        tree.key_handlers = {"ctrl+n": self.action_new_file}

    def action_toggle_hidden(self) -> None:
        self.show_hidden = not self.show_hidden
        tree = self.query_one(FilterableDirectoryTree)
        tree.show_hidden = self.show_hidden
        tree.reload()

        toggle_btn = self.query_one("#toggle_hidden")
        toggle_btn.label = "+" if self.show_hidden else "-"
        self.notify("Hidden files " + ("shown" if self.show_hidden else "hidden"))

    def action_toggle_sidebar(self) -> None:
        self.show_sidebar = not self.show_sidebar
        file_nav = self.query_one(".file-nav")
        if not self.show_sidebar:
            file_nav.add_class("hidden")
            # If the directory tree was focused, focus the code editor
            if self.app.focused is self.query_one(FilterableDirectoryTree):
                self.query_one(CodeEditor).focus()
        else:
            file_nav.remove_class("hidden")

    def action_focus_editor(self) -> None:
        self.query_one(CodeEditor).focus()

    def action_focus_tree(self) -> None:
        self.query_one(FilterableDirectoryTree).focus()

    def action_refresh_tree(self) -> None:
        tree = self.query_one(FilterableDirectoryTree)
        tree.refresh_tree()
        self.notify("Tree refreshed")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle_hidden":
            self.action_toggle_hidden()
            event.stop()
        elif event.button.id == "new_file":
            self.run_worker(self.editor.action_new_file())
            event.stop()
        elif event.button.id == "refresh_tree":
            self.action_refresh_tree()
            event.stop()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        try:
            # First check if it's a Python file by extension - this is a quick check to avoid binary detection, will implenent
            # a more robust solution later
            if str(event.path).endswith(".py"):
                editor = self.query_one(CodeEditor)
                editor.open_file(event.path)
                editor.focus()
                event.stop()
                return

            # For non-Python files, do binary detection
            with open(event.path, "rb") as file:
                # Read first chunk
                chunk = file.read(8192)

                # Common binary file signatures
                binary_signatures = [
                    b"\x7fELF",
                    b"MZ",
                    b"\x89PNG",
                    b"\xff\xd8\xff",
                    b"GIF",
                    b"BM",
                    b"PK",
                    b"\x1f\x8b",
                ]

                # Check for binary signatures
                if any(chunk.startswith(sig) for sig in binary_signatures):
                    self.notify("Cannot open binary file", severity="warning")
                    event.stop()
                    return

                # Check for null bytes, which definitively indicate binary files
                if b"\x00" in chunk:
                    self.notify("Cannot open binary file", severity="warning")
                    event.stop()
                    return

                # If no binary indicators found, try to decode as text file
                try:
                    chunk.decode("utf-8")
                    editor = self.query_one(CodeEditor)
                    editor.open_file(event.path)
                    editor.focus()
                    event.stop()
                except UnicodeDecodeError:
                    self.notify(
                        "Cannot open file: Not a valid UTF-8 text file",
                        severity="warning",
                    )
                    event.stop()

        except (IOError, OSError) as e:
            self.notify(f"Error opening file: {str(e)}", severity="error")
            event.stop()

    def get_initial_focus(self) -> Optional[Widget]:
        return self.query_one(FilterableDirectoryTree)


class CustomCodeEditor(CodeEditor):
    BINDINGS = [
        *CodeEditor.BINDINGS,
        Binding("shift+left", "focus_tree", "Focus Tree", show=True),
    ]

    def action_focus_tree(self) -> None:
        self.app.query_one("NestView").action_focus_tree()
