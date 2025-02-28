from typing import Dict, Optional, Tuple

import bilby
import matplotlib
import matplotlib.axes
import matplotlib.colorbar
import matplotlib.pyplot as plt
import numpy as np
from gwpy.plot import Plot
from gwpy.timeseries import TimeSeries
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_spectrogram_from_timeseries(
    timeseries: TimeSeries,
    q_value: Optional[float] = None,
    q_min: Optional[float] = None,
    q_max: Optional[float] = None,
    f_min: Optional[float] = 20,
    f_max: Optional[float] = None,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    time_resolution: Optional[float] = None,
    frequency_resolution: Optional[float] = None,
    whiten_timeseries: Optional[bool] = True,
    spectrogram_frequency_scale: Optional[str] = "log",
    colorbar_location: Optional[str] = "right",
    colormap: Optional[str] = "viridis",
    spectrogram_maximum_energy: Optional[float] = 25,
    fig_and_ax: Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]] = None,
    plot_kws: Optional[Dict] = None,
) -> Tuple[
    matplotlib.figure.Figure,
    matplotlib.axes.Axes,
    matplotlib.axes.Axes,
    matplotlib.colorbar.Colorbar,
    matplotlib.image.AxesImage,
]:
    """Produces a spectrogram given a gwpy TimeSeries, with some helpful manipulations.
    Descended with much modification from gwdetchar.scattering.plot._format_spectrogram.

    Parameters
    ==========
        timeseries : gwpy.timeseries.TimeSeries
            The timeseries from which the spectrogram will be produced
        q_value : Optional[float]
            A single value of q to fix for the Q transform which
            will generate the spectrogram.
            Exclusive with q_min and q_max
        q_min : Optional[float]
            A minimum value for the range of q values which
            gwpy will optimize over when performing the q transform.
            Requires q_max and exclusive with q_value
        q_max : Optional[float]
            A maximum value for the range of q values which
            gwpy will optimize over when performing the q transform.
            Requires q_min and exclusive with q_value
        f_min : Optional[float]
            A minimum value for the frequency range of the spectrogram.
            Defaults to standard minimum frequency of 20 Hz.
        f_max : Optional[float]
            A maximum value for the frequency range of the spectrogram.
            Defaults to Nyquist frequency.
        start_time : Optional[float]
            The start time for the output segment of the spectrogram
        end_time : Optional[float]
            The end time for the output segment of the spectrogram
        time_resolution : Optional[float]
            The time resolution for the q_transform, passed directly
            to the tres argument of `TimeSeries.q_transform`
        frequency_resolution : Optional[float]
            The frequency resolution for the q_transform, passed directly
            to the fres argument of `TimeSeries.q_transform`
        whiten_timeseries : Optional[bool]
            Whether the data needs to be whitened.
            Defaults True, assuming unwhitened data.
            If data is whitened pass this as False.
        spectrogram_frequency_scale : Optional[str]
            Options are "linear" and "log", defaults to "log"
        colorbar_location : Optional[str]
            The location of the colorbar relative to the spectrogram.
            Options are 'top', 'bottom', 'left', 'right'.
            Defaults to 'right'.
        colormap : Optional[str]
            The colormap to use, as matplotlib standard. Defaults to viridis.
        spectrogram_maximum_energy : Optional[float]
            The value at which the spectrogram saturates, i.e. the top of the color bar.
            Defaults to 25.
        fig_and_ax : Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
            The figure and axis object onto which the spectrogram is plotted.
            If not passed, these will be generated
        plot_kws : Optional[Dict]
            The dictionary of arguments for the Plot() call to make the figure and axes.

    Returns
    =======
        matplotlib.figure.Figure
            The figure object for the spectrogram
        matplotlib.axes.Axes
            The axes on which the spectrogram is plotted
        matplotlib.axes.Axes
            The axes on which the colorbar is plotted
        matplotlib.colorbar.Colorbar
            The colorbar object
        matplotlib.image.AxesImage
            The image of the spectrogram which was plotted`
    """
    # Infer the appropriate frequency range
    # Default to nyquist frequency as f_max
    f_max = 1 / 2 / timeseries.dt.value if f_max is None else f_max
    frequency_range = (f_min, f_max)

    # Infer the appropriate outseg
    # These settings will likely be a bit nasty if used, since
    # They will show the whole data segment
    start_time = timeseries.t0.value if start_time is None else start_time
    end_time = (
        timeseries.t0.value + timeseries.duration.value
        if end_time is None
        else end_time
    )
    outseg = (start_time, end_time)

    # Infer the q range based on inputs
    if q_value is not None and q_min is None and q_max is None:
        # If only q_value is set use that to fix the range
        q_range = (q_value, q_value)
    elif q_value is not None:
        # q_value is set and max or min is set, this is overspecified
        raise ValueError(
            "q range is overspecified, " "either fix a value or give a max and min"
        )
    elif q_min is not None and q_max is not None:
        # Set the range as requested
        q_range = (q_min, q_max)
    else:
        # Insufficient information
        raise ValueError(
            "q range is underspecified, " "either fix a value or give a max and min"
        )

    # Compute the q transform of the data
    qspecgram = timeseries.q_transform(
        qrange=q_range,
        frange=frequency_range,
        outseg=outseg,
        fres=frequency_resolution,
        tres=time_resolution,
        whiten=whiten_timeseries,
    )

    if fig_and_ax is None:
        plot_kws = {} if plot_kws is None else plot_kws
        fig = Plot(**plot_kws)
        ax = fig.add_subplot(111)
    else:
        fig, ax = fig_and_ax

    # Some tricks to plot the spectrogram and make the colorbar
    # While giving us control over its axes location
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(colorbar_location, size="5%", pad=0.05)
    im = ax.imshow(
        qspecgram,
        vmin=0,
        vmax=spectrogram_maximum_energy,
        cmap=colormap,
        norm="linear",
    )
    orientation = (
        "horizontal"
        if colorbar_location == "top" or colorbar_location == "bottom"
        else "vertical"
    )
    cb = fig.colorbar(im, cax=cax, orientation=orientation, label="Normalized Energy")
    if orientation == "horizontal":
        cax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        cax.xaxis.set_label_position("top")

    # Set scale and some universal labels
    ax.set_yscale(spectrogram_frequency_scale)
    ax.set_ylabel("Frequency [Hz]")
    ax.set_xlabel("Time [s]")

    return fig, ax, cax, cb, im
