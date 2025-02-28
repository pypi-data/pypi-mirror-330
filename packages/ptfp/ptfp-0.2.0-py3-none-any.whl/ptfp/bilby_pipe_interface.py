import copy
import os
from typing import Callable, Dict, Optional, Tuple

import bilby
import bilby_pipe
import bilby_pipe.data_analysis
import pandas as pd


def get_analysis_from_dag(
    path_to_dag: str,
    data_case: int = 0,
    data_analysis_input_class: Callable = bilby_pipe.data_analysis.DataAnalysisInput,
    parser_generator: Callable = bilby_pipe.parser.create_parser,
) -> bilby_pipe.data_analysis.DataAnalysisInput:
    """Given a dag (and located in the correct directory)
    gets the bilby_pipe.data_analysis.DataAnalysisInput object
    corresponding to that bilby pipe run.

    Parameters
    ==========
        path_to_dag : str
            The path to the dag, absolute or relative to
            directory from which it could be run
            (i.e. outdir/submit/dagname.dag)
        data_case : int
            The case of the data to use (i.e. the index 0
            in a ..._data0_... file name).
            For multiple injection runs, this is the injection
            index.

    Returns
    =======
        bibly_pipe.data_analysis.DataAnalysisInput
            The analysis input object corresponding to this run
    """
    with open(path_to_dag, "r") as f:
        lines = f.readlines()
        analysis_line = [
            x
            for x in lines
            if "VARS" in x
            and "analysis_H1L1" in x
            and f"data{data_case}_" in x
            and "par0" in x
        ][0]
        args, unknown_args = bilby_pipe.utils.parse_args(
            analysis_line.split('"')[1].split(" "),
            parser_generator(top_level=False),
        )
    analysis = data_analysis_input_class(args, unknown_args)
    return analysis


def draw_dict_sample_from_posterior(posterior: pd.DataFrame) -> Dict[str, float]:
    """Gets a correctly formatted dict corresponding to a single
    sample in the posterior.

    Parameters
    ==========
        posterior : pd.DataFrame
            The dataframe representation of the posterior
            to draw a sample from

    Returns
    =======
        Dict[str, float]
            The dictionary of {param_name : param_value} for a given sample
    """
    sample = posterior.sample()
    return {
        k: [v for v in sample_dict.values()][0]
        for k, sample_dict in sample.to_dict().items()
    }


def get_all_analysis_components(
    base_directory: str,
    analysis_ifos: Optional[str] = "H1L1",
    data_case: Optional[int] = 0,
) -> Tuple[
    bilby.core.result.Result,
    bilby_pipe.utils.DataDump,
    bilby_pipe.data_analysis.DataAnalysisInput,
    bilby.gw.likelihood.GravitationalWaveTransient,
]:
    """Reconstruct the objects used in the bilby pipe run
    by parsing out necessary information in the output directory,
    using various dag and file parsing methods.
    ***Requires the original run output directory to function***

    Parameters
    ==========
        base_directory : str
            The directory in which the analysis was run
        analysis_ifos : str
            The interferometers used for the analysis
            (as appears in bilby filenames)
        data_case : Optional[int]=0
            If there are multiple indexed data objects (e.g. from injections),
            this indexes which to return

    Returns
    =======
        bilby.core.result.Result
            The analysis result
        bilby_pipe.utils.DataDump
            The data dump object
        bilby_pipe.data_analysis.DataAnalysisInput
            The reconsructed analysis object
        bilby.gw.likelihood.GravitationalWaveTransient
            The likelihood used in the analysis
    """
    merge_result_file = [
        os.path.join(base_directory, "final_result", x)
        for x in os.listdir(os.path.join(base_directory, "final_result"))
        if f"data{data_case}_" in x and f"_{analysis_ifos}_" in x and "result.hdf5" in x
    ][0]
    result = bilby.core.result.read_in_result(merge_result_file)

    data_file = [
        os.path.join(base_directory, "data", x)
        for x in os.listdir(os.path.join(base_directory, "data"))
        if f"data{data_case}_" in x and "data_dump.pickle" in x
    ][0]
    data = bilby_pipe.utils.DataDump.from_pickle(data_file)

    owd = os.getcwd()
    os.chdir(os.path.join(base_directory, ".."))
    submit_dag = [
        os.path.join(base_directory, "submit", x)
        for x in os.listdir(os.path.join(base_directory, "submit"))
        if "dag" in x and x.split(".")[-1] == "submit"
    ][0]
    analysis = get_analysis_from_dag(submit_dag, data_case=data_case)
    os.chdir(owd)

    likelihood_args = [
        analysis.interferometers,
        analysis.waveform_generator,
    ]
    likelihood_kwargs = dict(
        priors=copy.deepcopy(result.priors), distance_marginalization=False
    )

    # We'll assume for this that it's always a GravitationalWaveTransient likelihood
    likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
        *likelihood_args, **likelihood_kwargs
    )

    return result, data, analysis, likelihood
