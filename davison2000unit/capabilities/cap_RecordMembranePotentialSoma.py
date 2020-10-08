import sciunit
from typing import Dict, List

class RecordMembranePotentialSoma(sciunit.Capability):
    """Enables recording membrane potential from soma"""

    def get_membrane_potential_soma(self, tstop: float):
        """Run simulation for time 'tstop', specified in ms, while recording
        the membrane potential from soma.
        Must return a list of the form:
        |    [ list1, list2 ] where,
        |        list1 = time series (in ms)
        |        list2 = membrane potential series (in mV)
        """
        raise NotImplementedError()

    def get_membrane_potential_soma_eFEL_format(self, tstop: float, start: float, stop: float) -> Dict[str, List[float]]:
        """Calls :meth:`get_membrane_potential_soma` and reformats
        its output structure into format accepted by eFEL library.
        Example of output format:
        .. code-block:: python
            efel_trace = {'T' : [time series in ms],
                          'V' : [somatic potential series in mv],
                          'stim_start' : [stimulus start time in ms],
                          'stim_end'   : [stimulus end time in ms]   }
        """
        traces = self.get_membrane_potential_soma(tstop)
        efel_trace = {'T' : traces[0],
                      'V' : traces[1],
                      'stim_start' : [start],
                      'stim_end'   : [stop]}
        return efel_trace