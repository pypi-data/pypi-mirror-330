import copy
from typing import Dict, Optional, Tuple

import bilby
import numpy as np
import pandas as pd


def get_projected_frequency_domain_waveform(
    parameters: Dict[str, float],
    waveform_generator: bilby.gw.waveform_generator.WaveformGenerator,
    interferometer: bilby.gw.detector.Interferometer,
) -> np.array:
    """Do the steps of getting and projecting the waveform,
    without adding it strain data

    Parameters
    ==========
        parameters : Dict[str, float]
            The dictionary of parameters for the waveform call
        waveform_generator : bilby.gw.waveform_generator.WaveformGenerator,
            The waveform generator to use
        interferometer : bilby.gw.detector.Interferometer
            The interferometer whose geometry should be used for the projection

    Returns
    =======
        np.array
            The frequency domain waveform, appropriately projected and conditioned
    """
    parameters = copy.copy(parameters)
    waveform_polarizations = waveform_generator.frequency_domain_strain(parameters)
    frequency_domain_waveform = interferometer.get_detector_response(
        waveform_polarizations, parameters
    )
    return frequency_domain_waveform


def get_waveform_posterior(
    posterior: pd.DataFrame,
    waveform_generator: bilby.gw.WaveformGenerator,
    interferometer: bilby.gw.detector.Interferometer,
    frequency_window_mask: Optional[np.array] = None,
    time_window_mask: Optional[np.array] = None,
    number_of_samples: Optional[int | None] = 500,
    seed: Optional[int] = None,
) -> Tuple[np.array, np.array, np.array, np.array]:
    """Produces a set of waveforms corresponding to the posterior,
    projected onto the interferometer and requested time/frequency window.
    Inherits some heavily refactored components of
    `bilby.gw.result.CBCResult.plot_interferometer_waveform_posterior()`

    Parameters
    ==========
        posterior : pd.DataFrame
            The set of configurations to process, likely `result.posterior`
            for some bilby.gw.result.CBCResult object
        waveform_generator : pd.DataFrame
            The waveform generator to ingest posterior configurations and
            produce waveform realizations
        interferometer : bilby.gw.detector.Interferometer
            The interferometer object onto which the waveforms are being projected
            and conditioned.
        frequency_window_mask : optional[np.array]
            The mask of the interferometer frequency array
            associated with frequencies of interest
        time_window_mask : optional[np.array]
            The mask of the interferometer time array
            associated with times of interest.
        number_of_samples : Optional[int | None]
            The number of samples to draw from the posterior when computing
            the waveform posterior. Used to reduce computation time. Defaults
            to 500, may pass None to use the full posterior.
        seed : Optional[int]
            If passed, sets a random seed for the sampling (see above)
            to get a consistent set of waveform draws.

    Returns
    =======
        np.array
            The *unwhitened* frequency domain strain for each sample,
            Each row corresponds to a different sample.
        np.array
            The *unwhitened* time domain strain for each sample,
            Each row corresponds to a different sample.
        np.array
            The *whitened* frequency domain strain for each sample,
            Each row corresponds to a different sample.
        np.array
            The *whitened* time domain strain for each sample,
            Each row corresponds to a different sample.
    """
    # Sample a subset of the posterior, or just take all of it
    if number_of_samples is None:
        samples = copy.deepcopy(posterior)
    elif number_of_samples <= len(posterior):
        samples = posterior.sample(number_of_samples, random_state=seed)
    else:
        samples = copy.deepcopy(posterior)

    # Set windowing mask to include everything by default
    frequency_window_mask = (
        np.ones(interferometer.frequency_array.shape, dtype=bool)
        if frequency_window_mask is None
        else frequency_window_mask
    )
    time_window_mask = (
        np.ones(interferometer.time_array.shape, dtype=bool)
        if time_window_mask is None
        else time_window_mask
    )

    # Prepare for each return set
    fd_waveforms = list()
    td_waveforms = list()
    fd_whitened_waveforms = list()
    td_whitened_waveforms = list()
    for _, params in samples.iterrows():
        params = params.to_dict()
        # First get projected FD waveform
        fd_waveform = get_projected_frequency_domain_waveform(
            parameters=params,
            waveform_generator=waveform_generator,
            interferometer=interferometer,
        )
        # Get regular TD waveform with ifft
        td_waveform = bilby.core.utils.infft(
            fd_waveform, interferometer.sampling_frequency
        )
        # Get whitened fd waveform
        fd_whitened_waveform = interferometer.whiten_frequency_series(fd_waveform)
        # Use that to get whitened td waveform
        td_whitened_waveform = (
            interferometer.get_whitened_time_series_from_whitened_frequency_series(
                fd_whitened_waveform
            )
        )

        # Set Nones for all undesired values
        fd_waveform[~frequency_window_mask] = None
        td_waveform[~time_window_mask] = None
        fd_whitened_waveform[~frequency_window_mask] = None
        td_whitened_waveform[~time_window_mask] = None

        # Add to respective lists, with appropriate downselection of time/frequency
        fd_waveforms.append(fd_waveform)
        td_waveforms.append(td_waveform)
        fd_whitened_waveforms.append(fd_whitened_waveform)
        td_whitened_waveforms.append(td_whitened_waveform)
    # Convert FD posteriors ASDs for meaningful plotting
    fd_waveforms = bilby.gw.utils.asd_from_freq_series(
        fd_waveforms, 1 / interferometer.strain_data.duration
    )
    fd_whitened_waveforms = bilby.gw.utils.asd_from_freq_series(
        fd_whitened_waveforms, 1 / interferometer.strain_data.duration
    )
    # Compose lists to arrays
    td_waveforms = np.array(td_waveforms)
    td_whitened_waveforms = np.array(td_whitened_waveforms)

    return fd_waveforms, td_waveforms, fd_whitened_waveforms, td_whitened_waveforms
