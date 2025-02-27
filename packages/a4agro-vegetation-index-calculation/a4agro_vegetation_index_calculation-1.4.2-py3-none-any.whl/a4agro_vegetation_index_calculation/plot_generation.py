import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import io
from matplotlib.colors import Normalize, LinearSegmentedColormap

matplotlib.use("Agg")  # Use non-interactive backend


def calculate_class_break_values(
    raster_array: np.ndarray, num_classes: int = 5, decimal_places: int = 4
) -> list[float]:
    valid_data = raster_array[~np.isnan(raster_array)]
    class_break_values = np.percentile(valid_data, np.linspace(0, 100, num_classes + 1))
    return np.round(class_break_values, decimal_places).tolist()


def generate_figure_save_and_show(
    index: np.ndarray, colormap_norm: tuple, show: bool = False
) -> io.BytesIO:
    colormap, norm = colormap_norm

    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    cbar_plot = ax.imshow(index, cmap=colormap, norm=norm, interpolation="nearest")
    ax.axis("off")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", pad_inches=0, bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)

    if show:
        plt.imshow(index, cmap=colormap, norm=norm)
        plt.show()

    return buf


def generate_figure_save_and_show_5_normalized(
    index: np.ndarray, colormap: LinearSegmentedColormap, show: bool = False
) -> io.BytesIO:
    min_val, max_val = np.nanmin(index), np.nanmax(index)
    norm = Normalize(vmin=min_val, vmax=max_val)

    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    
    cbar_plot = ax.imshow(index, cmap=colormap, norm=norm, interpolation="nearest")

    ax.axis("off")

    buf = io.BytesIO()
    fig.savefig(
        buf, format="png", pad_inches=0, bbox_inches="tight", transparent=True
    )
    plt.close(fig)
    buf.seek(0)

    if show:
        plt.imshow(index, cmap=colormap, norm=norm)
        plt.show()

    return buf