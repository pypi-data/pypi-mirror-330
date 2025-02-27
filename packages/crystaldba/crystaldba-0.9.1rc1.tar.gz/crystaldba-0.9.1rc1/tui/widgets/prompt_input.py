from dataclasses import dataclass
from typing import ClassVar
from typing import List

from textual import events
from textual import on
from textual.binding import Binding
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import TextArea


class PromptInput(TextArea):
    @dataclass
    class PromptSubmitted(Message):
        text: str
        prompt_input: "PromptInput"

    @dataclass
    class CursorEscapingTop(Message):
        pass

    @dataclass
    class CursorEscapingBottom(Message):
        pass

    BINDINGS: ClassVar[List[Binding]] = [
        Binding(
            "enter",
            "submit_prompt",
            "Send message",
            key_display="enter",
        ),
        Binding(
            "ctrl+j,alt+enter",
            "add_newline",
            "Newline",
            key_display="^j",
        ),
    ]

    submit_ready = reactive(True)

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled, language="markdown")

    def on_key(self, event: events.Key) -> None:
        if self.cursor_location == (0, 0) and event.key == "up":
            event.prevent_default()
            self.post_message(self.CursorEscapingTop())
            event.stop()
        elif self.cursor_at_end_of_text and event.key == "down":
            event.prevent_default()
            self.post_message(self.CursorEscapingBottom())
            event.stop()
        elif event.key == "ctrl+j":
            event.stop()
            event.prevent_default()
            insert = "\n"
            start, end = self.selection
            self._replace_via_keyboard(insert, start, end)
            return
        elif event.key == "enter":
            event.prevent_default()
            event.stop()
            self.action_submit_prompt()

    def action_add_newline(self) -> None:
        pass  # handled in self.on_key

    def action_submit_prompt(self) -> None:
        if self.text.strip() == "":
            self.notify("Cannot send empty message!")
            return

        if self.submit_ready:
            message = self.PromptSubmitted(self.text, prompt_input=self)
            self.clear()
            self.post_message(message)
        else:
            self.app.bell()
            self.notify("Please wait for response to complete.")

    def watch_submit_ready(self, submit_ready: bool) -> None:
        self.set_class(not submit_ready, "-submit-blocked")

    def on_mount(self):
        self.border_title = "Enter your [u]m[/]essage..."

    @on(TextArea.Changed)
    async def prompt_changed(self, event: TextArea.Changed) -> None:
        text_area = event.text_area
        if text_area.text.strip() != "":
            text_area.border_subtitle = "[white]^j[/white] Add a new line [white]enter[/white] Send message"
        else:
            text_area.border_subtitle = None

        text_area.set_class(text_area.wrapped_document.height > 1, "multiline")

        # TODO - when the height of the textarea changes
        #  things don't appear to refresh correctly.
        #  I think this may be a Textual bug.
        #  The refresh below should not be required.
        if self.parent is not None:
            self.parent.refresh()
