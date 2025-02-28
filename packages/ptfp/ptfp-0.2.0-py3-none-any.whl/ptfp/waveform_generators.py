from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd
from bilby.gw.waveform_generator import WaveformGenerator


class NegativeWaveformGenerator(WaveformGenerator):
    def __init__(
        self,
        parent=None,
        duration=None,
        sampling_frequency=None,
        start_time=0,
        frequency_domain_source_model=None,
        time_domain_source_model=None,
        parameters=None,
        parameter_conversion=None,
        waveform_arguments=None,
    ):
        """Initialize a negative waveform generator

        Parameters
        ==========
            parent : Optional[bilby.gw.waveform_generator.WaveformGenerator]
                If passed, uses this as the base waveform generator,
                then modifies the output.
                Obviates need for all other configuration.
            sampling_frequency : float, optional
                The sampling frequency
            duration : float, optional
                Time duration of data
            start_time : float, optional
                Starting time of the time array
            frequency_domain_source_model : func, optional
                A python function taking some arguments and returning the frequency
                domain strain. Note the first argument must be the frequencies at
                which to compute the strain
            time_domain_source_model : func, optional
                A python function taking some arguments and returning the time
                domain strain. Note the first argument must be the times at
                which to compute the strain
            parameters : dict, optional
                Initial values for the parameters
            parameter_conversion : func, optional
                Function to convert from sampled parameters to parameters of the
                waveform generator. Default value is the identity, i.e. it leaves
                the parameters unaffected.
            waveform_arguments : dict, optional
                A dictionary of fixed keyword arguments to pass to either
                `frequency_domain_source_model` or `time_domain_source_model`.

            Note: the arguments of frequency_domain_source_model (except the first,
            which is the frequencies at which to compute the strain) will be added to
            the WaveformGenerator object and initialised to `None`.
        """
        if parent is not None:
            self.__dict__ = parent.__dict__.copy()
        else:
            super(NegativeWaveformGenerator, self).__init__(
                duration,
                sampling_frequency,
                start_time,
                frequency_domain_source_model,
                time_domain_source_model,
                parameters,
                parameter_conversion,
                waveform_arguments,
            )

    def frequency_domain_strain(
        self, parameters: Optional[Dict[str, float]] = None
    ) -> Dict[str, np.array]:
        """Returns the negative frequency domain strain -h(f)

        Parameters
        ==========
            parameters : Optional[Dict[str, float]]
                The parameters of the sample to evaluate.
                If unpassed attempts to use waveform generator parameters

        Returns
        =======
            Dict[str, np.array]
                The strain dictionary of the negative
                e.g. {'plus':strain['plus'] * -1, 'cross':strain['cross'] * -1}
        """
        base_fd_strain = super().frequency_domain_strain(parameters)
        negative_fd_strain = {key: -1 * val for key, val in base_fd_strain.items()}
        return negative_fd_strain


class InjectionResidualWaveformGenerator(WaveformGenerator):
    """A waveform generator to inject the residual of a (PE)
    sample against an injection.
    That is, it injects h_inj - h_sample.
    This allows the production of residual posterior reconstructions
    """

    def __init__(
        self,
        injection_parameters: Dict[str, float],
        parent: Optional[WaveformGenerator] = None,
        duration: Optional[float] = None,
        sampling_frequency: Optional[float] = None,
        start_time: Optional[float] = 0,
        frequency_domain_source_model: Optional[Callable] = None,
        time_domain_source_model: Optional[Callable] = None,
        parameters: Optional[Dict[str, float]] = None,
        parameter_conversion: Optional[Callable] = None,
        waveform_arguments: Optional[Dict] = None,
    ):
        """Initialization for the residual generator

        Parameters
        ==========
            injection_parameters : Dict[str, float]
                The parameters used for the *injection*
            parent : Optional[bilby.gw.waveform_generator.WaveformGenerator]
                If passed, uses this as the base waveform generator,
                then modifies the output.
                Obviates need for all other configuration.
            sampling_frequency: float, optional
                The sampling frequency
            duration: float, optional
                Time duration of data
            start_time: float, optional
                Starting time of the time array
            frequency_domain_source_model: func, optional
                A python function taking some arguments and returning the frequency
                domain strain. Note the first argument must be the frequencies at
                which to compute the strain
            time_domain_source_model: func, optional
                A python function taking some arguments and returning the time
                domain strain. Note the first argument must be the times at
                which to compute the strain
            parameters: dict, optional
                Initial values for the parameters
            parameter_conversion: func, optional
                Function to convert from sampled parameters to parameters of the
                waveform generator. Default value is the identity, i.e. it leaves
                the parameters unaffected.
            waveform_arguments: dict, optional
                A dictionary of fixed keyword arguments to pass to either
                `frequency_domain_source_model` or `time_domain_source_model`.

                Note: the arguments of frequency_domain_source_model (except the first,
                which is the frequencies at which to compute the strain)
                will be added to the WaveformGenerator object
                and initialised to `None`.

        """
        if parent is not None:
            self.__dict__ = parent.__dict__.copy()
        else:
            super(InjectionResidualWaveformGenerator, self).__init__(
                duration,
                sampling_frequency,
                start_time,
                frequency_domain_source_model,
                time_domain_source_model,
                parameters,
                parameter_conversion,
                waveform_arguments,
            )
        self.injection_parameters = injection_parameters

    @property
    def injection_parameters(self) -> pd.DataFrame:
        """The parameters of the injection to take the residual against"""
        return self._injection_parameters

    @injection_parameters.setter
    def injection_parameters(self, injection_parameters: pd.DataFrame) -> None:
        self._injection_parameters = injection_parameters

    def frequency_domain_strain(
        self, parameters: Optional[Dict[str, float]] = None
    ) -> Dict[str, np.array]:
        """Returns the frequency domain residual strain (h_inj(f) - h_samp(f))

        Parameters
        ==========
            parameters : Optional[Dict[str, float]]
                The parameters of the sample to evaluate.
                If unpassed attempts to use waveform generator parameters

        Returns
        =======
            Dict[str, np.array]
                The strain dictionary of the residual (h_inj(f) - h_samp(f))
                e.g. {'plus':array, 'cross':array}
        """
        injection_fd_strain = super().frequency_domain_strain(self.injection_parameters)
        # get_detector_response will apply a timeshift based on *sample* parameters
        # so, proactively timeshift injection_fd_strain by the time difference
        dt = self.injection_parameters["geocent_time"] - parameters["geocent_time"]
        for mode, waveform in injection_fd_strain.items():
            injection_fd_strain[mode] = waveform * np.exp(
                -1j * 2 * np.pi * dt * self.frequency_array
            )
        estimated_fd_strain = super().frequency_domain_strain(parameters)
        return {
            key: injection_fd_strain[key] - val
            for key, val in estimated_fd_strain.items()
        }
