import numpy as np
from napari.layers import Shapes

from napari_vectorizer._widget import (
    label_vectorization_widget,
)


# make_napari_viewer is a pytest fixture that returns a napari viewer object
# you don't need to import it, as long as napari is installed
# in your testing environment
def test_label_vectorization_widget(make_napari_viewer):
    # Create a napari viewer
    viewer = make_napari_viewer()

    # Create a simple label layer with some labeled regions
    label_data = np.array(
        [[0, 0, 1, 1, 1], [0, 0, 1, 1, 0], [1, 0, 0, 1, 1], [1, 1, 0, 1, 1]],
        dtype=int,
    )
    label_layer = viewer.add_labels(label_data)

    # Instantiate the widget
    widget = label_vectorization_widget()

    # Execute widget function
    vectorized_layer = widget(label_layer, 0.5, 0.5)

    # Ensure output is a Shapes layer
    assert isinstance(
        vectorized_layer, Shapes
    ), "Output should be a Shapes layer"

    # Ensure some shapes were detected and created
    assert (
        len(vectorized_layer.data) > 0
    ), "Shapes layer should contain at least one shape"

    # Ensure shapes have correct properties
    for shape in vectorized_layer.data:
        assert (
            shape.shape[1] == 2
        ), "Each shape should contain (x, y) coordinates"

    # Ensure assigned face color is a valid vispy color
    assert (
        vectorized_layer.face_color is not None
    ), "Face color should be assigned"

    print("All tests passed!")
