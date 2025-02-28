from typing import Optional

import cv2 as cv
import numpy as np
from numpy.typing import NDArray
from PIL import ImageTk
from PIL import Image as PILImage

from widget_state import (
    BasicState,
    BoolState,
    HigherOrderState,
    StringState,
    compute,
    NumberState,
)

from ...state import PointState
from ...decorator import stateful
from .canvas import Canvas
from .lib import CanvasItem


class ImageData(BasicState[NDArray]):
    """
    ImageData is just a reactive container for a numpy array of an image"
    """

    def __init__(self, value: NDArray):
        super().__init__(value, verify_change=False)

        self.value = value

    def width(self):
        _width = NumberState(0)
        self.on_change(lambda _: _width.set(self.value.shape[1]), trigger=True)
        return _width

    def height(self):
        _height = NumberState(0)
        self.on_change(lambda _: _height.set(self.value.shape[0]), trigger=True)
        return _height


class ImageStyle(HigherOrderState):
    """
    Style properties of an image.

    * position: Define where the image center is placed in the canvas.
                The position is (0, 0) by default and is computed as the canvas
                center if `fit` is not None.
    * background: If True (the default) the image will be displayed behind all
                  other canvas items.
    * fit: If and how the image should fit the canvas dimensions. Possible
           values are ("none", "contain", "cover", "fill"). See
           `Image.compute_scales` for a description.
    """

    def __init__(
        self,
        position: Optional[PointState] = None,
        background: Optional[BoolState] = None,
        fit: Optional[StringState] = None,
    ):
        super().__init__()

        self.position = position if position is not None else PointState(0, 0)
        self.background = background if background is not None else BoolState(True)
        self.fit = fit if fit is not None else StringState("contain")


class ImageState(HigherOrderState):
    """
    ImageState that groups style and data in a reactive container.
    """

    def __init__(
        self,
        data: ImageData,
        style: Optional[ImageStyle] = None,
    ):
        super().__init__()

        self.data = data
        self.style = style if style is not None else ImageStyle()


def img_to_tk(img: np.ndarray) -> ImageTk:
    """
    Convert a numpy array in to tk image.
    """
    return ImageTk.PhotoImage(PILImage.fromarray(img))


@stateful
class Image(CanvasItem):
    """
    Draw an image onto a canvas.

    The class handles canvas resizing and contains utility methods
    to switch between canvas and image coordinates.

    Note: If a canvas is initialized with `width` and `height` properties,
    its size cannot increase beyond these values. Thus, it is better to
    implicitly define its dimensions via its parent.
    """

    def __init__(self, canvas: Canvas, state: ImageState):
        super().__init__(canvas, state)

        self.img_tk = None
        self.id = None
        self.data = self._state.data

        if state.style.fit.value != "none":
            state.style.position.depends_on(
                [canvas._state],
                lambda: PointState(
                    canvas._state.width.value // 2, canvas._state.height.value // 2
                ),
                kwargs={},
            )

        self.scale_x = self.scale_y = 1.0

    def array(self):
        return self._state.data.value

    def compute_scales(self) -> tuple[float, float]:
        """
        Compute scaling factors for the image depending on the fit mode.

        Fitting modes are similar to CSS properties.

        Mode:
          * fill: scale the image to fill the entire canvas
          * contain: keep the aspect ratio by choosing the smaller scale factor
          * cover: keep the aspect ratio and chose the larger scale factor

        Returns
        -------
        tuple of float
            scaling factors in x and y directions
        """
        scale_x = self.canvas._state.width.value / self._state.data.value.shape[1]
        scale_y = self.canvas._state.height.value / self._state.data.value.shape[0]

        fit = self._state.style.fit.value
        if fit == "fill":
            return scale_x, scale_y
        elif fit == "contain":
            scale_x = scale_y = min(scale_x, scale_y)
            return scale_x, scale_y
        elif fit == "cover":
            scale_x = scale_y = max(scale_x, scale_y)
            return scale_x, scale_y

        scale_x = scale_y = 1.0
        return scale_x, scale_y

    def draw(self, state: ImageState) -> None:
        self.scale_x, self.scale_y = self.compute_scales()

        self.img_tk = img_to_tk(
            cv.resize(state.data.value, None, fx=self.scale_x, fy=self.scale_y)
        )

        if self.id is None:
            self.id = self.canvas.create_image(
                *state.style.position.values(), image=self.img_tk
            )

        self.canvas.coords(self.id, *state.style.position.values())
        self.canvas.itemconfig(self.id, image=self.img_tk)

        if state.style.background.value:
            self.canvas.tag_lower(self.id)

    def point_to_canvas(self, pt: PointState) -> PointState:
        return compute(
            [self._state, pt],
            lambda: PointState(*self.to_canvas(pt.x.value, pt.y.value)),
        )

    def to_image(self, x: int, y: int) -> tuple[int, int]:
        """
        Transform x-, and y-coordinates from canvas space to image space.

        Parameters
        ----------
        x: int
        y: int

        Returns
        -------
        tuple[int, int]
        """
        x, y = self.to_image_continuous(x, y)
        x = round(x)
        y = round(y)
        return x, y

    def to_image_continuous(self, x: int, y: int) -> tuple[float, float]:
        """
        Transform x-, and y-coordinates from canvas space to image space.

        Parameters
        ----------
        x: int
        y: int

        Returns
        -------
        tuple[int, int]
        """
        image_width = self._state.data.value.shape[1]
        image_height = self._state.data.value.shape[0]

        t_x = (self.canvas._state.width.value - image_width * self.scale_x) // 2
        t_y = (self.canvas._state.height.value - image_height * self.scale_y) // 2

        x = (x - t_x) / self.scale_x
        y = (y - t_y) / self.scale_y
        return x, y

    def to_canvas(self, x: int | float, y: int | float) -> tuple[int, int]:
        """
        Transform x-, and y-coordinates from image space to canvas space.

        Parameters
        ----------
        x: int
        y: int

        Returns
        -------
        tuple[int, int]
        """
        image_width = self._state.data.value.shape[1]
        image_height = self._state.data.value.shape[0]

        t_x = (self.canvas._state.width.value - image_width * self.scale_x) // 2
        t_y = (self.canvas._state.height.value - image_height * self.scale_y) // 2

        x = round(x * self.scale_x + t_x)
        y = round(y * self.scale_y + t_y)

        return x, y
