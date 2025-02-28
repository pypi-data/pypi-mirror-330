from typing import Any, Dict, List, Optional, Tuple

import bilby
import gwpy
import matplotlib
import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np


def plot_time_domain_data(
    data: np.array,
    times: np.array,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    timeseries_plot_kws: Optional[dict] = None,
    fig_and_ax: Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]] = None,
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes, np.array]:
    """Plot an array of data in the time domain,
    and tracks what restricted times were plotted to.

    Parameters
    ==========
        data: np.array
            The data to be plotted. Could be
            gwpy.timeseries.TimeSeries.values.value
            or interferometer.strain_data.time_domain_strain
            or interferometer.whitened_time_domain_strain
        times: np.array
            The times corresponding to the data being plotted. Could be
            gwpy.timeseries.TimeSeries.times.value or
            interferometer.time_array
        start_time: Optional[float] = None
            The start time (absolute gps time) at which the plot should start.
            If not passed starts at first time in passed times array.
        end_time: Optional[float] = None
            The end time (absolute gps time) at which the plot should end.
            If not passed ends at last time in passed times array.
        timeseries_plot_kws : Optional[dict]
            The dictionary of keyword arguments to the ax.plot() call
            for the timeseries.
            See `matplotlib.axes.Axes.plot()` for optiosn.
        fig_and_ax: Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
            If passed, plots onto this ax object. Else makes its own.

    Returns
    =======
        matplotlib.figure.Figure
            The figure onto which the time series was plotted
        matplotlib.axes.Axes
            The axis onto which the time series was plotted
        np.array
            The boolean array for which points in the time array
            were plotted.
    """
    start_time = times[0] if start_time is None else start_time
    end_time = times[-1] if end_time is None else end_time

    time_mask = (times > start_time) & (times < end_time)

    if fig_and_ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = fig_and_ax

    timeseries_plot_kws = {} if timeseries_plot_kws is None else timeseries_plot_kws

    ax.plot(times[time_mask], data[time_mask], **timeseries_plot_kws)
    ax.set_xlabel("Time [s]")

    return fig, ax, time_mask


def plot_time_domain_posterior(
    posterior: np.array,
    times: np.array,
    posterior_color: Optional[str] = "C0",
    percentile_interval: Tuple[float, float] = (5, 95),
    median_alpha: Optional[float] = 1.0,
    credible_interval_alpha: Optional[float] = 0.3,
    posterior_label: Optional[str] = None,
    median_kws: Optional[Dict[str, Any]] = None,
    credible_interval_kws: Optional[Dict[str, Any]] = None,
    fig_and_ax: Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = None,
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
    """Plots a posterior time domain reconstruction.
    This adds the median as a line, then shades the requested credible interval.

    Parameters
    ==========
        posterior : np.array,
            The posterior of time domain realizations
        times : np.array,
            The array of times corresponding to the posterior.
            Could be obtained as `gwpy.timeseries.TimeSeries.times`
            from bilby.gw.detector.interferometer.Interferometer.time_array,
            or from other similar sources.
        posterior_color : Optional[str] = 'C0',
            The color for plotting the posterior
        percentile_interval : Tuple[float, float] = (5, 95),
            The minimum and maximum of the credible interval to plot.
            Defaults to (5,95) for a 90% credible intervals
        median_alpha : Optional[float] = 1,
            The alpha value of the plotted median of the posterior.
        credible_interval_alpha = 0.3,
            The alpha to apply to the credible interval portion of the
            posterior
        time_frequency_label : Optional[str] = None
            The label to use for the posterior.
            Will be processed for appropriate median and CI labels,
            formatted as e.g.
            "{time_frequency_label} Median" and
            "{time_frequency_label} {percentile_credible_interval}\\% Credible Interval"
        median_kws : Optional[Dict[str, Any]] = None
            If passed, supplies key word arguments to the .plot() call used to
            plot the median. These overwrite any choices inferred by previously passed
            arguments (e.g. 'color' will overwrite posterior_color)
        credible_interval_kws : Optional[Dict[str, Any]] = None
            If passed, supplies key word arguments to the .fill_between() call used to
            plot the credible intervals.
            These overwrite any choices inferred by previously passed
            arguments (e.g. 'color' will overwrite posterior_color)
        fig_and_ax : Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
            The figure and axis object onto which the posterior is plotted.
            If not passed, these will be generated

    Returns
    =======
        matplotlib.figure.Figure
            The figure object onto which the poserior was plotted.
        matplotlib.axes.Axes
            The axes object onto which the figure was plotted.
    """
    if posterior_label is not None:
        percentile_credible_interval = percentile_interval[1] - percentile_interval[0]
        median_interval_label = f"{posterior_label} Median"
        credible_interval_label = (
            f"{posterior_label}" f" {percentile_credible_interval}\\% Credible Interval"
        )
    else:
        median_interval_label = None
        credible_interval_label = None

    if fig_and_ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = fig_and_ax

    complete_median_kws = {
        "color": posterior_color,
        "label": median_interval_label,
        "alpha": median_alpha,
    }
    if median_kws is not None:
        complete_median_kws.update(median_kws)
    complete_credible_interval_kws = {
        "color": posterior_color,
        "label": credible_interval_label,
        "alpha": credible_interval_alpha,
    }
    if credible_interval_kws is not None:
        complete_credible_interval_kws.update(credible_interval_kws)

    # Plot the median and requested credible interval for the posterior
    ax.plot(times, np.nanmedian(posterior, axis=0), **complete_median_kws)
    ax.fill_between(
        times,
        np.nanpercentile(posterior, percentile_interval[0], axis=0),
        np.nanpercentile(posterior, percentile_interval[1], axis=0),
        **complete_credible_interval_kws,
    )

    ax.legend()

    return fig, ax


def force_axis_time_offset(
    ax: matplotlib.axes.Axes, new_ticks: List[float], tick_offset: float
):
    """Perform some tricks to make a time domain x-axis more palatable.
    Time domain plots from gwpy Timeseries objects will refer to the
    datetime, which produces a lot of ugly junk. Sometimes we may want to
    override and reference to the time segment instead.

    This does this by passing a set of ticks (that is, times to place ticks)
    as well as an offset. For example, if we have a 4 second duration and a merger
    at 1e9 + 2 seconds, and we want to have ticks at each second, we could do

    ```
    new_ticks = [0, 1, 2, 3, 4]
    tick_offset = 1e9
    ax = force_axis_time_offset(
        ax,
        new_ticks=new_ticks,
        tick_offset=tick_offset
    )
    ```

    This will result in an axis which labels 1e9 as 0, 1e9+1 as 1, etc.
    For time referenced to merger we could pass a list from [-2, 2] instead,
    and have a time offset of 1e9+2.

    Note that this *does not* alter the actual plotted content. If the
    data only covered a span of 0.5 seconds around the merger, but we passed the
    above ticks, there would be lots of empty content. So, it's still imperative to
    align the desired ticks with the plotted data segment.

    Parameters
    ==========
        ax : matplotlib.axes.Axes
            The axes object whose x-axis will be modified.
        new_ticks : List[float]
            The times of the new ticks. This should be the corresopnding data times
            minus the tick_offset
        tick_offset : float
            The offset of the new_ticks from the true data times (in gps time)

    Returns
    =======
        matplotlib.axes.Axes
            The axis object, now with modified x-axis

    """
    new_ticks = np.round(new_ticks, 4)
    labels = []
    for tick in new_ticks:
        labels.append(
            matplotlib.text.Text(
                tick + tick_offset, 0, "$\\mathdefault{" + str(tick) + "}$"
            )
        )
    new_ticks = [tick + tick_offset for tick in new_ticks]
    ax.set_xticks(new_ticks)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Time [s]")
    return ax
