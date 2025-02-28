from typing import Optional

import tkinter as tk
from widget_state import DictState, HigherOrderState, IntState, StringState

from ...state import PointState
from ...decorator import stateful
from .lib import CanvasItem


class TextStyle(DictState):

    def __init__(
        self,
        color: Optional[str | StringState] = None,
        anchor: Optional[str | StringState] = None,
        angle: Optional[int | IntState] = None,
        font_name: Optional[str | StringState] = None,
        font_size: Optional[int | IntState] = 12,
    ):
        super().__init__()

        self.color = color if isinstance(color, StringState) else StringState(color)
        self.anchor = anchor if isinstance(anchor, StringState) else StringState(anchor)
        self.angle = angle if isinstance(angle, IntState) else IntState(angle)
        self.font_name = (
            font_name if isinstance(font_name, StringState) else StringState(font_name)
        )
        self.font_size = (
            font_size if isinstance(font_size, IntState) else IntState(font_size)
        )


class TextData(HigherOrderState):

    def __init__(self, text: StringState, position: PointState):
        super().__init__()

        self.text = text
        self.position = position


class TextState(HigherOrderState):

    def __init__(self, data: TextData, style: Optional[TextStyle] = None):
        super().__init__()

        self.data = data
        self.style = style if style is not None else TextStyle()


@stateful
class Text(CanvasItem):
    def __init__(self, canvas: tk.Canvas, state: TextState):
        super().__init__(canvas, state)

        self.id = None

    def draw(self, state: TextState):
        if self.id is None:
            self.id = self.canvas.create_text(*state.data.position.values())

        self.canvas.coords(self.id, *state.data.position.values())
        self.canvas.itemconfig(
            self.id,
            text=state.data.text.value,
            fill=state.style.color.value,
            anchor=state.style.anchor.value,
            angle=state.style.angle.value,
            font=(state.style.font_name.value, state.style.font_size.value),
        )
