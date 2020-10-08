import os
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==============================================================================


class LogPlot:
    """
    Creates a log plot of 'Injected Current' vs 'Firing frequency' for specified data
    """

    def __init__(self, name="log_plot", score=None, params={}):
        self.filename = name
        self.score = score
        self.params = params

    def save_file(self):
        fig = plt.figure(figsize=(10, 7))

        obs_label = self.params["obs_label"] if "obs_label" in self.params else "observation"
        plt.loglog(list(self.score.observation.keys()), list(
            self.score.observation.values()), 'b', marker='s', markersize=8, label=obs_label)
        pred_label = self.params["pred_label"] if "pred_label" in self.params else "prediction"
        plt.loglog(list(self.score.prediction.keys()), list(
            self.score.prediction.values()), 'r', marker='o', markersize=8, label=pred_label)

        title = self.params["title"] if "title" in self.params else "Frequency"
        fig.suptitle(title, fontsize=20, fontweight='bold', y=1.035)
        xlim = self.params["xlim"] if "xlim" in self.params else None
        if xlim:
            plt.xlim(xlim)
        ylim = self.params["ylim"] if "ylim" in self.params else None
        if ylim:
            plt.ylim(ylim)
        xlabel = self.params["xlabel"] if "xlabel" in self.params else None
        if xlabel:
            plt.xlabel(xlabel, fontsize=18)
        ylabel = self.params["ylabel"] if "ylabel" in self.params else None
        if ylabel:
            plt.ylabel(ylabel, fontsize=18)

        ax = plt.gca()
        xticks = self.params["xticks"] if "xticks" in self.params else None
        if xticks:
            ax.set_xticks(xticks)
        xticklabels = self.params["xticklabels"] if "xticklabels" in self.params else None
        if xticklabels:
            ax.set_xticklabels(xticklabels)
        yticks = self.params["yticks"] if "yticks" in self.params else None
        if yticks:
            ax.set_yticks(yticks)
        yticklabels = self.params["yticklabels"] if "yticklabels" in self.params else None
        if yticklabels:
            ax.set_yticklabels(yticklabels)
        plt.tick_params(axis='both', which='major', labelsize=14)

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), prop={'size': 14})
        score_text = self.params["score_text"] if "score_text" in self.params else None
        if score_text:
            score_xy = self.params["score_xy"] if "score_xy" in self.params else (0.7, 0.1)
            plt.annotate(score_text, xy=score_xy, xycoords='axes fraction', weight='bold', size=14)

        fig.tight_layout()
        filepath = os.path.join(self.score.test.target_dir, self.filename + '.pdf')
        plt.savefig(filepath, dpi=600, bbox_inches = "tight")
        return filepath
