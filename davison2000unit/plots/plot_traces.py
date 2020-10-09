import os
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==============================================================================


class Traces:
    """
    Creates somatic membrane potential traces
    """

    def __init__(self, name="traces_plot", score=None, params={}):
        self.filename = name
        self.score = score
        self.params = params

    def save_file(self):
        size = len(self.score.test.traces)
        fig, axs = plt.subplots(size, figsize=(20, 7*size), squeeze=False)

        for ind, trace in enumerate(self.score.test.traces):
            axs[ind ,0].plot(trace["t"], trace["v"], label=str(trace["stim"])+" $\mu$A/cm$^2$")
            axs[ind, 0].legend(loc="best", prop={'size': 14})
            xlabel = self.params["xlabel"] if "xlabel" in self.params else None
            if xlabel:
                axs[ind, 0].set_xlabel(xlabel, fontsize=18)
            ylabel = self.params["ylabel"] if "ylabel" in self.params else None
            if ylabel:
                axs[ind, 0].set_ylabel(ylabel, fontsize=18)

        title = self.params["title"] if "title" in self.params else "Frequency"
        fig.suptitle(title, fontsize=20, fontweight='bold', y=1.0075)

        fig.tight_layout(h_pad=5)
        filepath = os.path.join(self.score.test.target_dir, self.filename + '.pdf')
        plt.savefig(filepath, dpi=600, bbox_inches = "tight")
        return filepath
