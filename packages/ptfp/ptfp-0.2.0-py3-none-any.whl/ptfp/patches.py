import matplotlib
import matplotlib.artist
import matplotlib.legend
import matplotlib.legend_handler
import matplotlib.offsetbox
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

# This comes directly from this stack exchange thread
# I don't know why it's not a standard matplotlib function,
# but oh well
# https://stackoverflow.com/questions/31908982/multi-color-legend-entry


# define an object that will be used by the legend
class MulticolorPatch(object):
    def __init__(self, colors: matplotlib.colors.Colormap):
        """A matplotlib patch containing multiple colors,
        for multi-color legend entries.
        Directly taken from
        https://stackoverflow.com/questions/31908982/multi-color-legend-entry

        Example usage:
        ```
        multicolor_patch = ptfp.patches.MulticolorPatch(colors)
        ax.legend(
            handles=[multicolor_patch],
            labels=labels,
            handler_map={
                ptfp.patches.MulticolorPatch: ptfp.patches.MulticolorPatchHandler()
            }
        )
        ```

        Parameters
        ==========
            colors : matplotlib.colors.Colormap
                The discrete colormap to make the patch from
        """
        self.colors = colors


# define a handler for the MulticolorPatch object
class MulticolorPatchHandler(object):
    """The handler for the multicolor patch"""

    def legend_artist(
        self,
        legend: matplotlib.legend.Legend,
        orig_handle: matplotlib.artist.Artist,
        fontsize: float,
        handlebox: matplotlib.offsetbox.OffsetBox,
    ):
        """The artist to use for illustrating the multicolor patch on the legend

        Parameters
        ==========
            legend: matplotlib.legend.Legend
                The legend to write the artist to
            orig_handle: matplotlib.artist.Artist
                The original artist in use
            fontsize: float
                The fonstize for the corresponding text
            handlebox: matplotlib.offsetbox.OffsetBox
                The box used to set the dimensions of the final illustration

        """
        width, height = handlebox.width, handlebox.height
        patches = []
        for i, c in enumerate(orig_handle.colors):
            patches.append(
                plt.Rectangle(
                    [
                        width / len(orig_handle.colors) * i - handlebox.xdescent,
                        -handlebox.ydescent,
                    ],
                    width / len(orig_handle.colors),
                    height,
                    facecolor=c,
                    edgecolor="none",
                )
            )

        patch = PatchCollection(patches, match_original=True)

        handlebox.add_artist(patch)
        return patch
