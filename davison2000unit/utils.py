import matplotlib.pyplot as plt
import os
import json
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

# ===============================================================================

def create_fig7(base_dir=None, model_list=[]):
    """Method to plot Fig. 7 from Davison et al., 2000

    This method will create a 2x2 multi-plot figure for soma and glom
    stimulation and recording of firing frequency and latency to first spike.

     Parameters
     ----------
     base_dir : string
         path to directory named 'validation_davison2000unit'
     model_list : list
         list of models to be plotted (2C, 3C, 4C); default is empty list and signifies all models

     Note
     ----
     Tested to work with default models names and default output directories

     Returns
     -------
     path
         The absolute path of the generated test output PDF figure

     Examples
     --------
     >>> fig7 = utils.create_fig7(base_dir = "./validation_davison2000unit")
     """

    if not base_dir:
        raise ValueError("'base_dir' not specified! Please specify the path to 'validation_davison2000unit'!")
    if type(model_list) is not list:
        raise ValueError("'model_list' must be specified as a list! Set to empty list for all models.")

    flag_2C = False
    flag_3C = False
    flag_4C = False
    if model_list == []:
        flag_2C = True
        flag_3C = True
        flag_4C = True
    else:
        if "2C" in model_list:
            flag_2C = True
        if "3C" in model_list:
            flag_3C = True
        if "4C" in model_list:
            flag_4C = True

    fig, axs = plt.subplots(2, 2, figsize=(10*2, 7*2))

    # ----------------------------------------------------------------------
    # SomaFiringFrequency

    json_soma_stim_freq = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim Firing Frequency", "2 Compartments", "soma_stim_freq.json")) as f:
            json_soma_stim_freq_2C = json.load(f)
        label_2C = json_soma_stim_freq_2C["pred_label"]
        json_soma_stim_freq[label_2C] = json_soma_stim_freq_2C["prediction"]
        label_full = json_soma_stim_freq_2C["obs_label"]
        json_soma_stim_freq[label_full] = json_soma_stim_freq_2C["observation"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim Firing Frequency", "3 Compartments", "soma_stim_freq.json")) as f:
            json_soma_stim_freq_3C = json.load(f)
        label_3C = json_soma_stim_freq_3C["pred_label"]
        json_soma_stim_freq[label_3C] = json_soma_stim_freq_3C["prediction"]
        if not flag_2C:
            label_full = json_soma_stim_freq_3C["obs_label"]
            json_soma_stim_freq[label_full] = json_soma_stim_freq_3C["observation"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim Firing Frequency", "4 Compartments", "soma_stim_freq.json")) as f:
            json_soma_stim_freq_4C = json.load(f)
        label_4C = json_soma_stim_freq_4C["pred_label"]
        json_soma_stim_freq[label_4C] = json_soma_stim_freq_4C["prediction"]
        if not flag_2C and not flag_3C:
            label_full = json_soma_stim_freq_4C["obs_label"]
            json_soma_stim_freq[label_full] = json_soma_stim_freq_4C["observation"]

    axs[0, 0].loglog(list(map(float, json_soma_stim_freq[label_full].keys())), list(
        json_soma_stim_freq[label_full].values()), 'b', marker='s', markersize=8, label=label_full)

    if flag_2C:
        axs[0, 0].loglog(list(map(float, json_soma_stim_freq[label_2C].keys())), list(
            json_soma_stim_freq[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[0, 0].loglog(list(map(float, json_soma_stim_freq[label_3C].keys())), list(
            json_soma_stim_freq[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[0, 0].loglog(list(map(float, json_soma_stim_freq[label_4C].keys())), list(
            json_soma_stim_freq[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[0, 0].set_title("Stimulus at Soma: Firing Frequency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[0, 0].set_xlim([0.15, 3.0])
    axs[0, 0].set_ylim([10.0, 200.0])
    axs[0, 0].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[0, 0].set_ylabel("Firing frequency (Hz)", fontsize=18)
    axs[0, 0].set_xticks([0.2, 0.4, 0.8, 1.6])
    axs[0, 0].set_xticklabels([0.2, 0.4, 0.8, 1.6])
    axs[0, 0].set_yticks([10, 100])
    axs[0, 0].set_yticklabels([10, 100])
    axs[0, 0].tick_params(axis='both', which='major', labelsize=14)
    axs[0, 0].legend(loc="best", prop={'size': 14})

    # ----------------------------------------------------------------------
    # GlomFiringFrequency

    json_glom_stim_freq = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim Firing Frequency", "2 Compartments", "glom_stim_freq.json")) as f:
            json_glom_stim_freq_2C = json.load(f)
        label_2C = json_glom_stim_freq_2C["pred_label"]
        json_glom_stim_freq[label_2C] = json_glom_stim_freq_2C["prediction"]
        label_full = json_glom_stim_freq_2C["obs_label"]
        json_glom_stim_freq[label_full] = json_glom_stim_freq_2C["observation"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim Firing Frequency", "3 Compartments", "glom_stim_freq.json")) as f:
            json_glom_stim_freq_3C = json.load(f)
        label_3C = json_glom_stim_freq_3C["pred_label"]
        json_glom_stim_freq[label_3C] = json_glom_stim_freq_3C["prediction"]
        if not flag_2C:
            label_full = json_glom_stim_freq_3C["obs_label"]
            json_glom_stim_freq[label_full] = json_glom_stim_freq_3C["observation"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim Firing Frequency", "4 Compartments", "glom_stim_freq.json")) as f:
            json_glom_stim_freq_4C = json.load(f)
        label_4C = json_glom_stim_freq_4C["pred_label"]
        json_glom_stim_freq[label_4C] = json_glom_stim_freq_4C["prediction"]
        if not flag_2C and not flag_3C:
            label_full = json_glom_stim_freq_4C["obs_label"]
            json_glom_stim_freq[label_full] = json_glom_stim_freq_4C["observation"]
    
    axs[0, 1].loglog(list(map(float, json_glom_stim_freq[label_full].keys())), list(
        json_glom_stim_freq[label_full].values()), 'b', marker='s', markersize=8, label=label_full)

    if flag_2C:
        axs[0, 1].loglog(list(map(float, json_glom_stim_freq[label_2C].keys())), list(
            json_glom_stim_freq[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[0, 1].loglog(list(map(float, json_glom_stim_freq[label_3C].keys())), list(
            json_glom_stim_freq[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[0, 1].loglog(list(map(float, json_glom_stim_freq[label_4C].keys())), list(
            json_glom_stim_freq[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[0, 1].set_title("Stimulus at Glomerulus: Firing Frequency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[0, 1].set_xlim([0.15, 3.0])
    axs[0, 1].set_ylim([10.0, 200.0])
    axs[0, 1].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[0, 1].set_ylabel("Firing frequency (Hz)", fontsize=18)
    axs[0, 1].set_xticks([0.2, 0.4, 0.8, 1.6])
    axs[0, 1].set_xticklabels([0.2, 0.4, 0.8, 1.6])
    axs[0, 1].set_yticks([10, 100])
    axs[0, 1].set_yticklabels([10, 100])
    axs[0, 1].tick_params(axis='both', which='major', labelsize=14)
    axs[0, 1].legend(loc="best", prop={'size': 14})

    # ----------------------------------------------------------------------
    # SomaFirstSpikeLatency

    json_soma_stim_latency = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim First Spike Latency", "2 Compartments", "soma_stim_latency.json")) as f:
            json_soma_stim_latency_2C = json.load(f)
        label_2C = json_soma_stim_latency_2C["pred_label"]
        json_soma_stim_latency[label_2C] = json_soma_stim_latency_2C["prediction"]
        label_full = json_soma_stim_latency_2C["obs_label"]
        json_soma_stim_latency[label_full] = json_soma_stim_latency_2C["observation"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim First Spike Latency", "3 Compartments", "soma_stim_latency.json")) as f:
            json_soma_stim_latency_3C = json.load(f)
        label_3C = json_soma_stim_latency_3C["pred_label"]
        json_soma_stim_latency[label_3C] = json_soma_stim_latency_3C["prediction"]
        if not flag_2C:
            label_full = json_soma_stim_latency_3C["obs_label"]
            json_soma_stim_latency[label_full] = json_soma_stim_latency_3C["observation"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim First Spike Latency", "4 Compartments", "soma_stim_latency.json")) as f:
            json_soma_stim_latency_4C = json.load(f)
        label_4C = json_soma_stim_latency_4C["pred_label"]
        json_soma_stim_latency[label_4C] = json_soma_stim_latency_4C["prediction"]
        if not flag_2C and not flag_3C:
            label_full = json_soma_stim_latency_4C["obs_label"]
            json_soma_stim_latency[label_full] = json_soma_stim_latency_4C["observation"]
    
    axs[1, 0].loglog(list(map(float, json_soma_stim_latency[label_full].keys())), list(
        json_soma_stim_latency[label_full].values()), 'b', marker='s', markersize=8, label=label_full)

    if flag_2C:
        axs[1, 0].loglog(list(map(float, json_soma_stim_latency[label_2C].keys())), list(
            json_soma_stim_latency[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[1, 0].loglog(list(map(float, json_soma_stim_latency[label_3C].keys())), list(
            json_soma_stim_latency[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[1, 0].loglog(list(map(float, json_soma_stim_latency[label_4C].keys())), list(
            json_soma_stim_latency[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[1, 0].set_title("Stimulus at Soma: First Spike Latency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[1, 0].set_xlim([0.15, 3.0])
    axs[1, 0].set_ylim([3.0, 150.0])
    axs[1, 0].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[1, 0].set_ylabel("First spike latency (ms)", fontsize=18)
    axs[1, 0].set_xticks([0.2, 0.4, 0.8, 1.6])
    axs[1, 0].set_xticklabels([0.2, 0.4, 0.8, 1.6])
    axs[1, 0].set_yticks([10, 100])
    axs[1, 0].set_yticklabels([10, 100])
    axs[1, 0].tick_params(axis='both', which='major', labelsize=14)
    axs[1, 0].legend(loc="best", prop={'size': 14})

    # ----------------------------------------------------------------------
    # GlomFirstSpikeLatency

    json_glom_stim_latency = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim First Spike Latency", "2 Compartments", "glom_stim_latency.json")) as f:
            json_glom_stim_latency_2C = json.load(f)
        label_2C = json_glom_stim_latency_2C["pred_label"]
        json_glom_stim_latency[label_2C] = json_glom_stim_latency_2C["prediction"]
        label_full = json_glom_stim_latency_2C["obs_label"]
        json_glom_stim_latency[label_full] = json_glom_stim_latency_2C["observation"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim First Spike Latency", "3 Compartments", "glom_stim_latency.json")) as f:
            json_glom_stim_latency_3C = json.load(f)
        label_3C = json_glom_stim_latency_3C["pred_label"]
        json_glom_stim_latency[label_3C] = json_glom_stim_latency_3C["prediction"]
        if not flag_2C:
            label_full = json_glom_stim_latency_3C["obs_label"]
            json_glom_stim_latency[label_full] = json_glom_stim_latency_3C["observation"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim First Spike Latency", "4 Compartments", "glom_stim_latency.json")) as f:
            json_glom_stim_latency_4C = json.load(f)
        label_4C = json_glom_stim_latency_4C["pred_label"]
        json_glom_stim_latency[label_4C] = json_glom_stim_latency_4C["prediction"]
        if not flag_2C and not flag_3C:
            label_full = json_glom_stim_latency_4C["obs_label"]
            json_glom_stim_latency[label_full] = json_glom_stim_latency_4C["observation"]

    axs[1, 1].loglog(list(map(float, json_glom_stim_latency[label_full].keys())), list(
        json_glom_stim_latency[label_full].values()), 'b', marker='s', markersize=8, label=label_full)

    if flag_2C:
        axs[1, 1].loglog(list(map(float, json_glom_stim_latency[label_2C].keys())), list(
            json_glom_stim_latency[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[1, 1].loglog(list(map(float, json_glom_stim_latency[label_3C].keys())), list(
            json_glom_stim_latency[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[1, 1].loglog(list(map(float, json_glom_stim_latency[label_4C].keys())), list(
            json_glom_stim_latency[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[1, 1].set_title("Stimulus at Glomerulus: First Spike Latency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[1, 1].set_xlim([0.15, 3.0])
    axs[1, 1].set_ylim([3.0, 150.0])
    axs[1, 1].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[1, 1].set_ylabel("First spike latency (ms)", fontsize=18)
    axs[1, 1].set_xticks([0.2, 0.4, 0.8, 1.6])
    axs[1, 1].set_xticklabels([0.2, 0.4, 0.8, 1.6])
    axs[1, 1].set_yticks([10, 100])
    axs[1, 1].set_yticklabels([10, 100])
    axs[1, 1].tick_params(axis='both', which='major', labelsize=14)
    axs[1, 1].legend(loc="best", prop={'size': 14})

    fig.tight_layout(h_pad=5, w_pad=5)
    filepath = os.path.join(os.path.abspath(base_dir), 'figure_7.pdf')
    plt.savefig(filepath, dpi=600, bbox_inches= "tight")
    return filepath

# ===============================================================================

def create_fig7_runtimes(base_dir=None, model_list=[]):
    """Method to plot run times for models from Davison et al., 2000

    This method will create a 2x2 multi-plot figure for run-times for the various simulations.

     Parameters
     ----------
     base_dir : string
         path to directory named 'validation_davison2000unit'
     model_list : list
         list of models to be plotted (2C, 3C, 4C); default is empty list and signifies all models

     Note
     ----
     Tested to work with default models names and default output directories

     Returns
     -------
     path
         The absolute path of the generated test output PDF figure

     Examples
     --------
     >>> fig7 = utils.create_fig7_runtimes(base_dir = "./validation_davison2000unit")
     """

    if not base_dir:
        raise ValueError("'base_dir' not specified! Please specify the path to 'validation_davison2000unit'!")
    if type(model_list) is not list:
        raise ValueError("'model_list' must be specified as a list! Set to empty list for all models.")

    flag_2C = False
    flag_3C = False
    flag_4C = False
    if model_list == []:
        flag_2C = True
        flag_3C = True
        flag_4C = True
    else:
        if "2C" in model_list:
            flag_2C = True
        if "3C" in model_list:
            flag_3C = True
        if "4C" in model_list:
            flag_4C = True

    fig, axs = plt.subplots(2, 2, figsize=(10*2, 7*2))

    # ----------------------------------------------------------------------
    # SomaFiringFrequency

    json_soma_stim_freq = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim Firing Frequency", "2 Compartments", "soma_stim_freq.json")) as f:
            json_soma_stim_freq_2C = json.load(f)
        label_2C = json_soma_stim_freq_2C["pred_label"]
        json_soma_stim_freq[label_2C] = json_soma_stim_freq_2C["run_times"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim Firing Frequency", "3 Compartments", "soma_stim_freq.json")) as f:
            json_soma_stim_freq_3C = json.load(f)
        label_3C = json_soma_stim_freq_3C["pred_label"]
        json_soma_stim_freq[label_3C] = json_soma_stim_freq_3C["run_times"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim Firing Frequency", "4 Compartments", "soma_stim_freq.json")) as f:
            json_soma_stim_freq_4C = json.load(f)
        label_4C = json_soma_stim_freq_4C["pred_label"]
        json_soma_stim_freq[label_4C] = json_soma_stim_freq_4C["run_times"]

    if flag_2C:
        axs[0, 0].plot(list(map(float, json_soma_stim_freq[label_2C].keys())), list(
            json_soma_stim_freq[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[0, 0].plot(list(map(float, json_soma_stim_freq[label_3C].keys())), list(
            json_soma_stim_freq[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[0, 0].plot(list(map(float, json_soma_stim_freq[label_4C].keys())), list(
            json_soma_stim_freq[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[0, 0].set_title("Stimulus at Soma: Firing Frequency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[0, 0].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[0, 0].set_ylabel("Real time (s)", fontsize=18)
    axs[0, 0].tick_params(axis='both', which='major', labelsize=14)
    axs[0, 0].legend(loc="best", prop={'size': 14})

    # ----------------------------------------------------------------------
    # GlomFiringFrequency

    json_glom_stim_freq = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim Firing Frequency", "2 Compartments", "glom_stim_freq.json")) as f:
            json_glom_stim_freq_2C = json.load(f)
        label_2C = json_glom_stim_freq_2C["pred_label"]
        json_glom_stim_freq[label_2C] = json_glom_stim_freq_2C["run_times"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim Firing Frequency", "3 Compartments", "glom_stim_freq.json")) as f:
            json_glom_stim_freq_3C = json.load(f)
        label_3C = json_glom_stim_freq_3C["pred_label"]
        json_glom_stim_freq[label_3C] = json_glom_stim_freq_3C["run_times"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim Firing Frequency", "4 Compartments", "glom_stim_freq.json")) as f:
            json_glom_stim_freq_4C = json.load(f)
        label_4C = json_glom_stim_freq_4C["pred_label"]
        json_glom_stim_freq[label_4C] = json_glom_stim_freq_4C["run_times"]
    
    if flag_2C:
        axs[0, 1].plot(list(map(float, json_glom_stim_freq[label_2C].keys())), list(
            json_glom_stim_freq[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[0, 1].plot(list(map(float, json_glom_stim_freq[label_3C].keys())), list(
            json_glom_stim_freq[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[0, 1].plot(list(map(float, json_glom_stim_freq[label_4C].keys())), list(
            json_glom_stim_freq[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[0, 1].set_title("Stimulus at Glomerulus: Firing Frequency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[0, 1].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[0, 1].set_ylabel("Real time (s)", fontsize=18)
    axs[0, 1].tick_params(axis='both', which='major', labelsize=14)
    axs[0, 1].legend(loc="best", prop={'size': 14})

    # ----------------------------------------------------------------------
    # SomaFirstSpikeLatency

    json_soma_stim_latency = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim First Spike Latency", "2 Compartments", "soma_stim_latency.json")) as f:
            json_soma_stim_latency_2C = json.load(f)
        label_2C = json_soma_stim_latency_2C["pred_label"]
        json_soma_stim_latency[label_2C] = json_soma_stim_latency_2C["run_times"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim First Spike Latency", "3 Compartments", "soma_stim_latency.json")) as f:
            json_soma_stim_latency_3C = json.load(f)
        label_3C = json_soma_stim_latency_3C["pred_label"]
        json_soma_stim_latency[label_3C] = json_soma_stim_latency_3C["run_times"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Soma Stim First Spike Latency", "4 Compartments", "soma_stim_latency.json")) as f:
            json_soma_stim_latency_4C = json.load(f)
        label_4C = json_soma_stim_latency_4C["pred_label"]
        json_soma_stim_latency[label_4C] = json_soma_stim_latency_4C["run_times"]
    
    if flag_2C:
        axs[1, 0].plot(list(map(float, json_soma_stim_latency[label_2C].keys())), list(
            json_soma_stim_latency[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[1, 0].plot(list(map(float, json_soma_stim_latency[label_3C].keys())), list(
            json_soma_stim_latency[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[1, 0].plot(list(map(float, json_soma_stim_latency[label_4C].keys())), list(
            json_soma_stim_latency[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[1, 0].set_title("Stimulus at Soma: First Spike Latency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[1, 0].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[1, 0].set_ylabel("Real time (s)", fontsize=18)
    axs[1, 0].tick_params(axis='both', which='major', labelsize=14)
    axs[1, 0].legend(loc="best", prop={'size': 14})

    # ----------------------------------------------------------------------
    # GlomFirstSpikeLatency

    json_glom_stim_latency = {}
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim First Spike Latency", "2 Compartments", "glom_stim_latency.json")) as f:
            json_glom_stim_latency_2C = json.load(f)
        label_2C = json_glom_stim_latency_2C["pred_label"]
        json_glom_stim_latency[label_2C] = json_glom_stim_latency_2C["run_times"]
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim First Spike Latency", "3 Compartments", "glom_stim_latency.json")) as f:
            json_glom_stim_latency_3C = json.load(f)
        label_3C = json_glom_stim_latency_3C["pred_label"]
        json_glom_stim_latency[label_3C] = json_glom_stim_latency_3C["run_times"]
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Glom Stim First Spike Latency", "4 Compartments", "glom_stim_latency.json")) as f:
            json_glom_stim_latency_4C = json.load(f)
        label_4C = json_glom_stim_latency_4C["pred_label"]
        json_glom_stim_latency[label_4C] = json_glom_stim_latency_4C["run_times"]

    if flag_2C:
        axs[1, 1].plot(list(map(float, json_glom_stim_latency[label_2C].keys())), list(
            json_glom_stim_latency[label_2C].values()), 'm', marker='+', mew=3, markersize=10, label=label_2C)

    if flag_3C:
        axs[1, 1].plot(list(map(float, json_glom_stim_latency[label_3C].keys())), list(
            json_glom_stim_latency[label_3C].values()), 'g', marker='x', mew=3, markersize=8, label=label_3C)

    if flag_4C:
        axs[1, 1].plot(list(map(float, json_glom_stim_latency[label_4C].keys())), list(
            json_glom_stim_latency[label_4C].values()), 'r', marker='o', markersize=8, label=label_4C)

    axs[1, 1].set_title("Stimulus at Glomerulus: First Spike Latency", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    axs[1, 1].set_xlabel("Injected current ($\mu$A/cm$^2$)", fontsize=18)
    axs[1, 1].set_ylabel("Real time (s)", fontsize=18)
    axs[1, 1].tick_params(axis='both', which='major', labelsize=14)
    axs[1, 1].legend(loc="best", prop={'size': 14})

    fig.tight_layout(h_pad=5, w_pad=5)
    filepath = os.path.join(os.path.abspath(base_dir), 'figure_runtimes.pdf')
    plt.savefig(filepath, dpi=600, bbox_inches= "tight")
    return filepath

# ===============================================================================

def create_fig_runtimes(base_dir=None, model_list=[]):
    """Method to plot run times for models from Davison et al., 2000

    This method will create a bar plot of all models with data from Test 'RunTime' .

     Parameters
     ----------
     base_dir : string
         path to directory named 'validation_davison2000unit'
     model_list : list
         list of models to be plotted (2C, 3C, 4C); default is empty list and signifies all models

     Note
     ----
     Tested to work with default models names and default output directories

     Returns
     -------
     path
         The absolute path of the generated test output PDF figure

     Examples
     --------
     >>> fig = utils.create_fig_runtimes(base_dir = "./validation_davison2000unit")
     """

    if not base_dir:
        raise ValueError("'base_dir' not specified! Please specify the path to 'validation_davison2000unit'!")
    if type(model_list) is not list:
        raise ValueError("'model_list' must be specified as a list! Set to empty list for all models.")

    flag_2C = False
    flag_3C = False
    flag_4C = False
    if model_list == []:
        flag_2C = True
        flag_3C = True
        flag_4C = True
    else:
        if "2C" in model_list:
            flag_2C = True
        if "3C" in model_list:
            flag_3C = True
        if "4C" in model_list:
            flag_4C = True

    fig = plt.figure(figsize=(10, 7))
    ax = plt.gca()

    json_run_time_labels = []
    json_run_time_scores = []
    json_run_time_colors = []
    if flag_2C:
        with open(os.path.join(os.path.abspath(base_dir), "Run Time", "2 Compartments", "run_time.json")) as f:
            json_run_time_2C = json.load(f)
        json_run_time_labels.append(json_run_time_2C["pred_label"])
        json_run_time_scores.append(json_run_time_2C["score"])
        json_run_time_colors.append("m")
    if flag_3C:
        with open(os.path.join(os.path.abspath(base_dir), "Run Time", "3 Compartments", "run_time.json")) as f:
            json_run_time_3C = json.load(f)
        json_run_time_labels.append(json_run_time_3C["pred_label"])
        json_run_time_scores.append(json_run_time_3C["score"])
        json_run_time_colors.append("g")
    if flag_4C:
        with open(os.path.join(os.path.abspath(base_dir), "Run Time", "4 Compartments", "run_time.json")) as f:
            json_run_time_4C = json.load(f)
        json_run_time_labels.append(json_run_time_4C["pred_label"])
        json_run_time_scores.append(json_run_time_4C["score"])
        json_run_time_colors.append("r")

    ax.bar(json_run_time_labels, json_run_time_scores, width = 0.5, color = json_run_time_colors)
    for i, v in enumerate(json_run_time_scores):
        ax.text(i - 0.05, v + 0.05 , str(round(v, 2)), color=json_run_time_colors[i], fontsize=14, fontweight='bold')
   
    ax.set_title("Compare Run Times", {"fontsize": 20, "fontweight" : "bold"}, pad=25)
    ax.set_ylabel("Model", fontsize=18)
    ax.set_ylabel("Real time (s)", fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=14)

    fig.tight_layout(h_pad=5, w_pad=5)
    filepath = os.path.join(os.path.abspath(base_dir), 'figure_runtimes.pdf')
    plt.savefig(filepath, dpi=600, bbox_inches= "tight")
    return filepath
