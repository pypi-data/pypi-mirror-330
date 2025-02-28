from typing import Optional

import matplotlib


def set_better_matplotlib_defaults(
    fontsize: Optional[float] = 16,
    plot_type: Optional[str] = "row",
    x_size: Optional[float] = None,
    aspect_ratio: Optional[float] = 1,
    legend_fontsize: Optional[float] = None,
    use_seaborn_colorblind_palette: Optional[bool] = True,
):
    """Sets useful plotting defaults, courtesy of Derek Davis.
    I have no idea where they got them from.
    These are simply a starting point, and one should of course modify
    these settings subsequently in the given application if desired.

    Parameters
    ==========
        fontsize : Optional[float]
            The standard fontsize to use.
            Should vary depending where the plot ends up!
            Larger fontsizes for talks, smaller
            (though still not too small)
            for papers.
        plot_type : Optional[str]
            The type of plot - row or column.
            This fixes the x_size to 6.75 or 3.375 respectively.
        x_size : Optional[float]
            If desiring a value other than the standard
            row or column for the x_size, may pass here.
            Overrides plot_type.
        aspect_ratio : Optional[float]
            The ratio x/y. The size of the x axis is referenced by the type of plot.
            The size of y will be x / aspect_ratio.
        legend_fontsize : Optional[float]
            The fontsize for the legend, defaults to half of standard fontsize.
        use_seaborn_colorblind_palette : Optional[bool] = True
            As the name describes, whether to set the colorpalette to
            the seaborn colorblind scheme.
    """
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    # ALWAYS USE figsize = (3.375, X) for column plots
    # figsize = (6.75, X) for rows
    # This
    if x_size is not None:
        pass
    else:
        x_size = 3.375 if plot_type == "column" else 6.75
    y_size = x_size / aspect_ratio

    # Set the legend fontsize smaller by default
    legend_fontsize = 3 * fontsize / 4 if legend_fontsize is None else legend_fontsize

    params = {
        "axes.labelsize": fontsize,
        "font.size": fontsize,
        "legend.fontsize": legend_fontsize,
        "xtick.labelsize": fontsize,
        "ytick.labelsize": fontsize,
        "axes.titlesize": fontsize,
        "lines.linewidth": 0.75,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "text.usetex": True,
        "font.family": "Serif",
        "font.serif": "Computer Modern Roman",
        "axes.grid": True,
        "figure.figsize": (x_size, y_size),
        "figure.dpi": 250,
    }

    for param in params.keys():
        matplotlib.rcParams[param] = params[param]

    if use_seaborn_colorblind_palette:
        import seaborn as sns

        sns.set_palette("colorblind")
