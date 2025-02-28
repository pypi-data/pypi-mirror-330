import copy
from typing import Any, Dict, List, Optional, Tuple

import bilby
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pycbc.filter import resample_to_delta_t
from pycbc.types.timeseries import TimeSeries as PyCBCTimeSeries
from pycbc.waveform import get_td_waveform
from pycbc.waveform.utils import frequency_from_polarizations
from scipy.signal import savgol_filter

BILBY_TO_PYCBC_CONVENTION_MAP = {
    "mass_1": "mass1",
    "mass_2": "mass2",
    "spin_1x": "spin1x",
    "spin_1y": "spin1y",
    "spin_1z": "spin1z",
    "spin_2x": "spin2x",
    "spin_2y": "spin2y",
    "spin_2z": "spin2z",
    "luminosity_distance": "distance",
    "phase": "coa_phase",
    "iota": "inclination",
    "ra": "ra",
    "dec": "dec",
    "psi": "psi",
    "geocent_time": "geocent_time",
}

PYCBC_TO_BILBY_CONVENTION_MAP = {
    val: key for key, val in BILBY_TO_PYCBC_CONVENTION_MAP.items()
}
BASE_SAMPLE_RATE = 1.0 / 16384 / 2


def low_pass_filter(
    input_time_domain_data: np.array,
    low_pass_limit: float = BASE_SAMPLE_RATE / 2,
    sampling_rate: int = BASE_SAMPLE_RATE,
) -> np.array:
    """Low pass filters a numpy array of time domain data.
    Slight modifications from code by Derek Davis.

    Parameters
    ==========
        input_time_domain_data : np.array
            The time domain data to low pass filter
        low_pass_limit : float
            The boundary of the low pass filter
        sampling_rate : sampling_rate
            The sampling rate of the input time domain data

    Returns
    =======
        np.array
            The time domain data, low pass filtered

    """
    # Infer the index of the limit
    bandlimit_index = int(low_pass_limit * input_time_domain_data.size / sampling_rate)

    # Go to FD
    fsig = np.fft.fft(input_time_domain_data)

    # Zero out everything above the pass limit
    for i in range(bandlimit_index + 1, len(fsig) - bandlimit_index):
        fsig[i] = 0

    # Return to TD
    filtered_time_domain_data = np.fft.ifft(fsig)

    return np.real(filtered_time_domain_data)


def time_frequency_track_from_bilby_components(
    sample: Dict[str, float],
    interferometer: bilby.gw.detector.interferometer.Interferometer,
    waveform_generator: bilby.gw.waveform_generator.WaveformGenerator,
    mode_array: List[List[int]] = [[2, 2], [2, -2]],
    relative_time_of_track_start: Optional[float] = None,
    relative_time_of_track_end: Optional[float] = None,
    smoothing_lowpass_limit: Optional[float] = 30,
    savgol_window_length: Optional[int] = 61,
    savgol_polyorder: Optional[int] = 1,
) -> np.array:
    """Produces an (approximate) time-frequency track for a bilby sample.

    Parameters
    ==========
        sample : Dict[str, float]
            The sample for which the track will be determined, as drawn from
            a bilby posterior.
        interferometer : bilby.gw.detector.interferometer.Interferometer
            The interferometer object used for determining projection properties.
        waveform_generator : bilby.gw.waveform_generator.WaveformGenerator
            The waveform generator which would generate the desired waveform,
            used to determine corresponding pycbc properties.
        mode_array: List[List[int, int]] = [[2, 2], [2, -2]]
            The modes to use in the computation. Waveforms with higher modes
            break SPA (used in this determination) when used directly,
            so by default this downselects to only the (2, \\pm 2) modes.
        relative_time_of_track_start : Optional[float] = None
            An optional parameter to force the start of the track, since
            behavior before minimum frequency can be odd.
            Referenced to interferometer start time.
        relative_time_of_track_end : Optional[float] = None
            An optional parameter to force an end of the track, since
            behavior post-ringdown becomes odd. Referenced to interferometer
            start time.
        smoothing_lowpass_limit : Optional[float] = 30
            The bound for lowpassing f(t), which may otherwise be unstable.
        savgol_window_length : Optional[int]= 61
            The window length passed to `scipy.signal.savgol_filter` for smoothing.
            Default is an empirically determined value.
        savgol_polyorder : Optional[int] = 1
            The polyorder paseed to `scipy.signal.savgol_filter`.
            Default is to an empirically determined value.

    Returns
    =======
        np.array
            The frequency as a function of time for the sample. Indices
            correspond to interferometer.time_array.
    """
    # Infer interferometer time
    sample[f"{interferometer.name}_time"] = (
        interferometer.time_delay_from_geocenter(
            sample["ra"], sample["dec"], sample["geocent_time"]
        )
        + sample["geocent_time"]
    )
    # Convert to pycbc convention and get a pycbc waveform
    pycbc_sample = {
        BILBY_TO_PYCBC_CONVENTION_MAP[key]: sample[key]
        for key in BILBY_TO_PYCBC_CONVENTION_MAP.keys()
    }
    plus, cross = get_td_waveform(
        approximant=waveform_generator.waveform_arguments["waveform_approximant"],
        f_lower=waveform_generator.waveform_arguments["minimum_frequency"],
        mode_array=mode_array,
        f_ref=waveform_generator.waveform_arguments["reference_frequency"],
        **pycbc_sample,
        delta_t=BASE_SAMPLE_RATE,
    )

    # Handle timing convention
    plus.start_time += sample[f"{interferometer.name}_time"]
    cross.start_time += sample[f"{interferometer.name}_time"]

    # Downsample as necessary
    if waveform_generator.sampling_frequency != BASE_SAMPLE_RATE:
        plus = resample_to_delta_t(plus, 1 / waveform_generator.sampling_frequency)
        cross = resample_to_delta_t(cross, 1 / waveform_generator.sampling_frequency)

    # Use SPA implementation to get an (approximate) f(t)
    # It is necessary to take the absolute value because
    # pycbc gives the frequency evolution as negative for face off configurations
    # Which is undesirable
    frequency_as_a_function_of_time = np.abs(frequency_from_polarizations(plus, cross))

    # Put it into the right timeseries
    interferometer_time_array = PyCBCTimeSeries(
        np.zeros(int(interferometer.duration * interferometer.sampling_frequency)),
        delta_t=1 / interferometer.sampling_frequency,
        epoch=interferometer.start_time,
    )
    frequency_as_a_function_of_time = interferometer_time_array.add_into(
        frequency_as_a_function_of_time
    )

    # Do some smoothing, since for precessing systems it can get very nasty
    smoothed_frequency_as_a_function_of_time = savgol_filter(
        low_pass_filter(
            frequency_as_a_function_of_time.numpy().flatten(),
            low_pass_limit=smoothing_lowpass_limit,
            sampling_rate=1 / waveform_generator.sampling_frequency,
        ),
        window_length=savgol_window_length,
        polyorder=savgol_polyorder,
    )

    # Some waveforms produce non-zero but very small nonsense
    # before the waveform actually starts, and after it ends.
    # This finds the indices where that is the case
    # and uses them to clean up the timeseries
    # This trick relies on the fact that (for (2,2)) plus and cross
    # Will have a pi / 4 phase offset
    # Such that the sum of the two won't have any zero crossings
    direct_injection_for_zeroing = interferometer_time_array.add_into(plus)
    direct_injection_for_zeroing = interferometer_time_array.add_into(cross)

    zeroing_indices = np.isclose(
        direct_injection_for_zeroing.numpy() / direct_injection_for_zeroing.max(),
        0,
        atol=1e-3,
    )
    smoothed_frequency_as_a_function_of_time[zeroing_indices] = None

    # If requested, force beginnings and ends
    if relative_time_of_track_start is not None:
        smoothed_frequency_as_a_function_of_time[
            frequency_as_a_function_of_time.sample_times
            < relative_time_of_track_start + interferometer.start_time
        ] = None
    if relative_time_of_track_end is not None:
        smoothed_frequency_as_a_function_of_time[
            frequency_as_a_function_of_time.sample_times
            > relative_time_of_track_end + interferometer.start_time
        ] = None

    return smoothed_frequency_as_a_function_of_time


def time_frequency_posterior_from_bilby_components(
    posterior: pd.DataFrame,
    interferometer: bilby.gw.detector.interferometer.Interferometer,
    waveform_generator: bilby.gw.waveform_generator.WaveformGenerator,
    number_of_samples: Optional[int] = 500,
    mode_array: List[List[int]] = [[2, 2], [2, -2]],
    relative_time_of_track_start: Optional[float] = None,
    relative_time_of_track_end: Optional[float] = None,
    smoothing_lowpass_limit: Optional[float] = 30,
    savgol_window_length: Optional[int] = 61,
    savgol_polyorder: Optional[int] = 1,
    seed: Optional[int] = None,
) -> np.array:
    """Produces an array of time-frequency tracks for a posterior

    Parameters
    ==========
        posterior: pd.DataFrame
            A posterior of configurations from which to generate
            time-frequency tracks.
        interferometer : bilby.gw.detector.interferometer.Interferometer
            The interferometer object used for determining projection properties.
        waveform_generator : bilby.gw.waveform_generator.WaveformGenerator
            The waveform generator which would generate the desired waveform,
            used to determine corresponding pycbc properties.
        number_of_samples : Optional[int]
            The number of samples to draw from the posterior. If None will use
            the whole posterior, and if number_of_samples > len(posterior)
            will use the whole posterior.
        mode_array: List[List[int, int]] = [[2, 2], [2, -2]]
            The modes to use in the computation. Waveforms with higher modes
            break SPA (used in this determination) when used directly,
            so by default this downselects to only the (2, \\pm 2) modes.
        relative_time_of_track_start : Optional[float] = None
            An optional parameter to force the start of the track, since
            behavior before minimum frequency can be odd.
            Referenced to interferometer start time.
        relative_time_of_track_end : Optional[float] = None
            An optional parameter to force an end of the track, since
            behavior post-ringdown becomes odd. Referenced to interferometer
            start time.
        smoothing_lowpass_limit : Optional[float] = 30
            The bound for lowpassing f(t), which may otherwise be unstable.
        savgol_window_length : Optional[int]= 61
            The window length passed to `scipy.signal.savgol_filter` for smoothing.
            Default is an empirically determined value.
        savgol_polyorder : Optional[int] = 1
            The polyorder paseed to `scipy.signal.savgol_filter`.
            Default is to an empirically determined value.
        seed : Optional[int]
            If passed will fix the seed used for sampling the posterior, for
            reproducibility.
        fig_and_ax : Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
            The figure and axis object onto which the posterior is plotted.
            If not passed, these will be generated
    Returns
    =======
        np.array
            The frequency as a function of time for each sample in the posterior.
            Has shape (number_of_samples, len(interferometer.time_array))
    """
    # Sample a subset of the posterior, or just take all of it
    if number_of_samples is None:
        samples = copy.deepcopy(posterior)
    elif number_of_samples <= len(posterior):
        samples = posterior.sample(number_of_samples, random_state=seed)
    else:
        samples = copy.deepcopy(posterior)

    # Iterate over samples
    time_frequency_tracks = []
    for _, sample in samples.iterrows():
        time_frequency_tracks.append(
            time_frequency_track_from_bilby_components(
                sample=sample,
                interferometer=interferometer,
                waveform_generator=waveform_generator,
                mode_array=mode_array,
                relative_time_of_track_start=relative_time_of_track_start,
                relative_time_of_track_end=relative_time_of_track_end,
                smoothing_lowpass_limit=smoothing_lowpass_limit,
                savgol_window_length=savgol_window_length,
                savgol_polyorder=savgol_polyorder,
            )
        )
    time_frequency_tracks = np.array(time_frequency_tracks)

    return time_frequency_tracks


def plot_time_frequency_posterior(
    time_frequency_posterior: np.array,
    time_array: np.array,
    color: Optional[str] = "C0",
    percentile_interval: Tuple[float, float] = (5, 95),
    median_alpha: Optional[float] = 1.0,
    credible_interval_alpha: Optional[float] = 0.3,
    time_frequency_label: Optional[str] = None,
    median_kws: Optional[Dict[str, Any]] = None,
    credible_interval_kws: Optional[Dict[str, Any]] = None,
    fig_and_ax: Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]] = None,
) -> matplotlib.axes.Axes:
    """Given an f(t) posterior, such as computed by
    `time_frequency_posterior_from_bilby_components`,
    Plot the median and credible interval on the given
    axis object

    Parameters
    ==========
        time_frequency_posterior : np.array,
            The posterior on time-frequency realizations to plot
        time_array : np.array,
            The array of times corresponding to the f(t) posterior.
            Could be obtained as `gwpy.timeseries.TimeSeries.times`
            from bilby.gw.detector.interferometer.Interferometer.time_array,
            or from other similar sources.
        color : Optional[str] = 'C0',
            The color for plotting the posterior
        percentile_interval : Tuple[float, float] = (5, 95),
            The minimum and maximum of the credible interval to plot.
            Defaults to (5,95) for a 90% credible intervals
        median_alpha : Optional[float] = 1,
            The alpha value of the plotted median track.
        credible_interval_alpha = 0.3,
            The alpha to apply to the credible interval portion of the
            time-frequency posterior
        time_frequency_label : Optional[str] = None
            The label to use for the time-frequency posterior.
            Will be processed for appropriate median and CI labels,
            formatted as e.g.
            "{time_frequency_label} Median" and
            "{time_frequency_label} {percentile_credible_interval}\\% Credible Interval"
        median_kws : Optional[Dict[str, Any]] = None
            If passed, supplies key word arguments to the .plot() call used to
            plot the median. These overwrite any choices inferred by previously passed
            arguments
            (e.g. 'label' here will overwrite the label inferred for the median)
        credible_interval_kws : Optional[Dict[str, Any]] = None
            If passed, supplies key word arguments to the .fill_between() call used to
            plot the credible intervals.
            These overwrite any choices inferred by previously passed
            arguments
            (e.g. 'label' will overwrite the label inferred for the credible interval)
    fig_and_ax: Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = None,
        fig_and_ax : Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
            The figure and axis object onto which the posterior is plotted.
            If not passed, these will be generated

    Returns
    =======
        ax : matplotlib.axes.Axes
            The axes object with the time-frequency posterior plotted onto it.
    """

    # If there is a desired label, infer variations for median and 90% CI
    # Otherwise don't write anything
    if time_frequency_label is not None:
        percentile_credible_interval = percentile_interval[1] - percentile_interval[0]
        median_interval_label = f"{time_frequency_label} Median"
        credible_interval_label = (
            f"{time_frequency_label}"
            f" {percentile_credible_interval}\\% Credible Interval"
        )
    else:
        median_interval_label = None
        credible_interval_label = None

    if fig_and_ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = fig_and_ax

    complete_median_kws = {
        "color": color,
        "label": median_interval_label,
        "alpha": median_alpha,
    }
    if median_kws is not None:
        complete_median_kws.update(median_kws)

    complete_credible_interval_kws = {
        "color": color,
        "label": credible_interval_label,
        "alpha": credible_interval_alpha,
    }
    if credible_interval_kws is not None:
        complete_credible_interval_kws.update(credible_interval_kws)

    # Store the original ylim from the spectrogram, so the track won't force it
    # Into a blank region
    original_ylim = ax.get_ylim()

    # Plot the median and requested credible interval for the posterior
    ax.plot(
        time_array,
        np.nanmedian(time_frequency_posterior, axis=0),
        **complete_median_kws,
    )
    ax.fill_between(
        time_array,
        np.nanpercentile(time_frequency_posterior, percentile_interval[0], axis=0),
        np.nanpercentile(time_frequency_posterior, percentile_interval[1], axis=0),
        **complete_credible_interval_kws,
    )

    ax.set_ylim(*original_ylim)
    if time_frequency_label is not None:
        ax.legend()
    return ax


def plot_time_frequency_track(
    time_frequency_track: np.array,
    time_array: np.array,
    track_kws: Dict = None,
    fig_and_ax: Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]] = None,
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
    """Given an f(t) timeseries, plot it on a time-frequency
    domain plot (e.g. a spectrogram).
    Plot the median and credible interval on the given
    axis object

    Parameters
    ==========
        time_frequency_track : np.array,
            The time-frequency track to plot
        time_array : np.array
            The array of times corresponding to the f(t) track.
            Could be obtained as `gwpy.timeseries.TimeSeries.times`
            from bilby.gw.detector.interferometer.Interferometer.time_array,
            or from other similar sources.
        track_kws : Dict
            The dictionary of keyword arguments passed to ax.plot().
        fig_and_ax : Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]
            The figure and axis object onto which the track is plotted.
            If not passed, these will be generated

    Returns
    =======
        matplotlib.figure.Figure
            The figure object with the time-frequency track overplotted
        matplotlib.axes.Axes
            The axes object with the time-frequency track plotted onto it.
    """
    # If there is a desired label, infer variations for median and 90% CI
    # Otherwise don't write anything
    track_kws = {} if track_kws is None else track_kws

    if fig_and_ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = fig_and_ax

    # Store the original ylim from the spectrogram, so the track won't force it
    # Into a blank region
    original_ylim = ax.get_ylim()

    ax.plot(time_array, time_frequency_track, **track_kws)

    ax.set_ylim(*original_ylim)
    if "label" in track_kws:
        ax.legend()

    return fig, ax
