import tkinter as tk
from typing import Optional

from widget_state import HigherOrderState, IntState, StringState

from ...decorator import stateful


class CanvasState(HigherOrderState):

    def __init__(
        self,
        width: Optional[IntState] = None,
        height: Optional[IntState] = None,
        background_color: Optional[StringState] = None,
    ):
        super().__init__()

        self.width = width if width is not None else IntState(None)
        self.height = height if height is not None else IntState(None)
        self.background_color = (
            background_color if background_color is not None else StringState(None)
        )


@stateful
class Canvas(tk.Canvas):

    def __init__(self, parent: tk.Widget, state: CanvasState):
        super().__init__(parent)

        self._state.width.value = int(self["width"])
        self._state.height.value = int(self["height"])

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # the event width and height values contain border width and
        # other contributions that we need to exclude
        border_width = int(self["bd"])
        highlight_thickness = int(self["highlightthickness"])
        self._state.width.value = event.width - 2 * (border_width + highlight_thickness)
        self._state.height.value = event.height - 2 * (
            border_width + highlight_thickness
        )

    def draw(self, state):
        self.config(
            background=state.background_color.value,
        )
