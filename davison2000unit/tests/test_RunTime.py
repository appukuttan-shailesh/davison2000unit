import os
import json
import numpy
import timeit
import sciunit
import davison2000unit.capabilities as cap
import davison2000unit.plots as plots
from sciunit.scores import FloatScore
from typing import Dict, Optional

import functools

# ===============================================================================


class RunTime(sciunit.Test):
    """Evaluate the model run time"""

    score_type: sciunit.scores = FloatScore
    """specifies the type of score returned by the test"""

    description = (
        "Evaluate the model run time for a simulation of one minute.")
    """brief description of the test objective"""

    def __init__(self,
                 observation: Dict[str, float] = {},
                 name: str = "Run Time",
                 output_dir: str = ".") -> None:
        self.required_capabilities += (cap.InjectStepCurrentSoma,
                                       cap.RecordMembranePotentialSoma)
        sciunit.Test.__init__(self, observation, name)
        self.output_dir = output_dir

    # ----------------------------------------------------------------------

    def validate_observation(self, observation: float) -> None:
        try:
            assert (isinstance(observation, int) or isinstance(observation, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must be a number!"))

    # ----------------------------------------------------------------------

    def run_stim(self, model: sciunit.Model, stim: float):
        stim_start = 50.0            # ms
        stim_dur = (60*1000) - 50.0  # ms
        stim_amp = stim              # nA
        model.inject_step_current_soma(current={'delay': stim_start,
                                                'duration': stim_dur,
                                                'amplitude': stim_amp})
        start = timeit.default_timer()
        trace = model.get_membrane_potential_soma_eFEL_format(tstop=stim_start+stim_dur,
                                                              start=stim_start,
                                                              stop=stim_start+stim_dur)
        stop = timeit.default_timer()
        run_time = stop - start
        self.traces.append({"stim" : stim_amp, 
                            "t" : trace["T"], 
                            "v" : trace["V"]})
        return run_time

    def generate_prediction(self, model: sciunit.Model) -> float:
        self.traces = []

        stim_inj = 0.4
        prediction = self.run_stim(model, stim_inj)
        return prediction

    # ----------------------------------------------------------------------

    def compute_score(self, observation: float, prediction: float, verbose: bool = False) -> FloatScore:
        # print("observation = {}".format(observation))
        # print("prediction = {}".format(prediction))
        self.figures = []
        runtime = FloatScore(prediction-observation)
        runtime.description = "Time (in seconds) required to complete simulation"
        return runtime

    # ----------------------------------------------------------------------

    def bind_score(self, score: FloatScore, model: sciunit.Model, observation: float, prediction: float):
        # create output directory
        self.target_dir = os.path.join(os.path.abspath(self.output_dir), "validation_davison2000unit", self.name, model.name)
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # create relevant output files
        # 1. JSON data: observation, prediction, score
        validation_data = {
            "pred_label": score.model.name,
            "observation": observation,
            "prediction": prediction,
            "score": score.score,
        }
        with open(os.path.join(self.target_dir, 'run_time.json'), 'w') as f:
            json.dump(validation_data, f, indent=4)

        # 2. JSON data: save Vm vs t trace
        with open(os.path.join(self.target_dir, 'run_time_trace.json'), 'w') as f:
            json.dump(self.traces, f, indent=4)

        # 3. Vm trace as pdf: somatic Vm trace during simulation
        params = {
            "title": "Somatic Vm: Stimulus at Soma",
            "xlabel": "Time (ms)",
            "ylabel": "Membrane potential (mV)"
        }
        traces_plot = plots.Traces(name="run_time_trace", score=score, params=params)
        file_traces_plot = traces_plot.save_file()
        self.figures.append(file_traces_plot)

        score.related_data["figures"] = self.figures
        return score
