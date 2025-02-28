"""
This module contains a napari widgets declared using a magic_factory decorated function:

References:
- Widget specification: https://napari.org/stable/plugins/guides.html?#widgets
- magicgui docs: https://pyapp-kit.github.io/magicgui/

"""

import random
from typing import TYPE_CHECKING

import numpy as np
from magicgui import magic_factory
from napari.layers import Shapes
from skimage.measure import approximate_polygon, find_contours
from vispy.color import get_color_names

if TYPE_CHECKING:
    import napari


# the magic_factory decorator lets us customize aspects of our widget
# we specify a widget type for the threshold parameter
# and use auto_call=True so the function is called whenever
# the value of a parameter changes
@magic_factory(
    contours_tolerance={
        "widget_type": "FloatSpinBox",
        "value": 0.5,
        "min": 0.00,
        "max": 0.99,
    },
    polygon_tolerance={
        "widget_type": "FloatSpinBox",
        "value": 0.5,
        "min": 0.00,
    },
)
def label_vectorization_widget(
    label_layer: "napari.layers.Labels",
    contours_tolerance: "float",
    polygon_tolerance: "float",
) -> "napari.layers.Shapes":
    # finding contours on padded image (to get outer contours of edge features too)
    padding_size = 1
    contours = [
        np.maximum(contour - 1, 0)
        for contour in find_contours(
            np.pad(label_layer.data, padding_size), contours_tolerance
        )
    ]
    # simplifing shapes
    polygons = [
        approximate_polygon(contour, polygon_tolerance) for contour in contours
    ]

    return Shapes(
        polygons,
        shape_type="polygon",
        face_color=random.choice(get_color_names()),
    )
