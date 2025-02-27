from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import TabbedContent, TabPane

from posting.widgets.request.header_editor import HeaderEditor
from posting.widgets.request.query_editor import QueryStringEditor
from posting.widgets.request.request_body import RequestBodyTextArea
from posting.widgets.request.request_options import RequestOptions
from posting.widgets.text_area import TextAreaFooter, TextEditor


class RequestEditorTabbedContent(TabbedContent):
    BINDINGS = [
        Binding("down,j", "app.focus_next", "Focus next", show=False),
        Binding("up,k", "app.focus_previous", "Focus previous", show=False),
    ]


class RequestEditor(Vertical):
    """
    The request editor.
    """

    def compose(self) -> ComposeResult:
        with Vertical() as vertical:
            vertical.border_title = "Request"
            with RequestEditorTabbedContent():
                with TabPane("Headers", id="headers-pane"):
                    yield HeaderEditor()
                with TabPane("Body", id="body-pane"):
                    text_area = RequestBodyTextArea(language="json")
                    yield TextEditor(
                        text_area=text_area,
                        footer=TextAreaFooter(text_area),
                    )
                with TabPane("Parameters", id="parameters-pane"):
                    yield QueryStringEditor()
                with TabPane("Options", id="options-pane"):
                    yield RequestOptions()

    def on_mount(self):
        self.border_title = "Request"
        self.add_class("section")
