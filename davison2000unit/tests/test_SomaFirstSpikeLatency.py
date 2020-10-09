import os
import efel
import json
import numpy
import timeit
import sciunit
import davison2000unit.capabilities as cap
import davison2000unit.plots as plots
from davison2000unit.scores import RMSscore
from typing import Dict, Optional

import functools
# import multiprocessing
# from multiprocessing import Pool

# ===============================================================================


class SomaFirstSpikeLatency(sciunit.Test):
    """Test latency to first spike at soma when stimulated at soma"""

    score_type: sciunit.scores = RMSscore
    """specifies the type of score returned by the test"""

    description = (
        "Evaluate the latency to first spike at soma under step current stimulus at soma of varying intensities")
    """brief description of the test objective"""

    def __init__(self,
                 observation: Dict[str, float] = {},
                 name: str = "Soma Stim First Spike Latency",
                 output_dir: str = ".") -> None:
        self.required_capabilities += (cap.InjectStepCurrentSoma,
                                       cap.RecordMembranePotentialSoma)
        sciunit.Test.__init__(self, observation, name)
        self.output_dir = output_dir

    # ----------------------------------------------------------------------

    def validate_observation(self, observation: Dict[str, float]) -> None:
        try:
            for key, val in observation.items():
                assert (isinstance(key, str))
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'amp1': lat1, 'amp2': lat2, ...}"))

    # ----------------------------------------------------------------------

    def run_stim(self, model: sciunit.Model, stim: float):
        stim_start = 50.0   # ms
        stim_dur = 150.0    # ms
        stim_amp = stim     # nA
        model.inject_step_current_soma(current={'delay': stim_start,
                                                'duration': stim_dur,
                                                'amplitude': stim_amp})
        start = timeit.default_timer()
        trace = model.get_membrane_potential_soma_eFEL_format(tstop=stim_start+stim_dur,
                                                              start=stim_start,
                                                              stop=stim_start+stim_dur)
        stop = timeit.default_timer()
        self.run_times[str(stim)] = stop - start
        self.traces.append({"stim" : stim_amp, 
                            "t" : trace["T"], 
                            "v" : trace["V"]})
        result = efel.getFeatureValues([trace], ["time_to_first_spike"])[
            0]["time_to_first_spike"][0] # (ms)
        return result

    def generate_prediction(self, model: sciunit.Model) -> Dict[float, float]:
        self.traces = []
        self.run_times = {}
        efel.reset()
        stim_list = list(map(float, self.observation.keys()))
        run_stim_ = functools.partial(self.run_stim, model)

        # multiprocessing giving errors regards to [xcb] ?!
        # npool = multiprocessing.cpu_count() - 1
        # with Pool(npool, maxtasksperchild=1) as pool:
        # results = pool.map(run_stim_, stim_list, chunksize=1)

        results = []
        for stim_inj in stim_list:
            results.append(run_stim_(stim_inj))

        # construct prediction with structure similar to observation
        prediction = {}
        for ind, stim_inj in enumerate(stim_list):
            prediction[stim_inj] = results[ind]
        return prediction

    # ----------------------------------------------------------------------

    def compute_score(self, observation: Dict[float, float], prediction: Dict[float, float], verbose: bool = False) -> RMSscore:
        # print("observation = {}".format(observation))
        # print("prediction = {}".format(prediction))
        self.figures = []
        rms = RMSscore.compute(list(observation.values()), list(prediction.values()))
        score = self.score_type(rms.score)
        score.description = "Root Mean Square (RMS) of difference between observation and prediction for each stimulus"
        return score

    # ----------------------------------------------------------------------

    def bind_score(self, score: RMSscore, model: sciunit.Model, observation: Dict[float, float], prediction: Dict[float, float]):
        # create output directory
        self.target_dir = os.path.join(os.path.abspath(self.output_dir), "validation_davison2000unit", self.name, model.name)
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # create relevant output files
        # 1. JSON data: observation, prediction, score, run_times
        validation_data = {
            "obs_label": "Full model",
            "pred_label": score.model.name,
            "observation": observation,
            "prediction": prediction,
            "score": score.score,
            "run_times" : self.run_times
        }
        with open(os.path.join(self.target_dir, 'soma_stim_latency.json'), 'w') as f:
            json.dump(validation_data, f, indent=4)

        # 2. Log plot as pdf: observation vs prediction
        params = {
            "title": "Stimulus at Soma: First Spike Latency",
            "obs_label": "Full model",
            "pred_label": score.model.name,
            "xlim": [0.15, 3.0],
            "ylim": [3.0, 150.0],
            "xlabel": "Injected current ($\mu$A/cm$^2$)",
            "ylabel": "First spike latency (ms)",
            "xticks": [0.2, 0.4, 0.8, 1.6],
            "xticklabels": [0.2, 0.4, 0.8, 1.6],
            "yticks": [10, 100],
            "yticklabels": [10, 100],
            "score_text": "RMS Score = " + str(round(score.score, 2)),
            "score_xy": (0.7, 0.7)
        }
        log_plot = plots.LogPlot(name="soma_stim_latency", score=score, params=params)
        file_log_plot = log_plot.save_file()
        self.figures.append(file_log_plot)

        # 3. JSON data: save Vm vs t traces
        with open(os.path.join(self.target_dir, 'soma_stim_latency_traces.json'), 'w') as f:
            json.dump(self.traces, f, indent=4)

        # 4. Vm traces as pdf: superimpose somatic Vm traces for all stimuli
        params = {
            "title": "Somatic Vm: Stimulus at Soma",
            "xlabel": "Time (ms)",
            "ylabel": "Membrane potential (mV)"
        }
        traces_plot = plots.Traces(name="soma_stim_latency_traces", score=score, params=params)
        file_traces_plot = traces_plot.save_file()
        self.figures.append(file_traces_plot)

        score.related_data["figures"] = self.figures
        return score