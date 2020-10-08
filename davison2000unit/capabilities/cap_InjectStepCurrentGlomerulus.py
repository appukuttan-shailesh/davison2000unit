import sciunit

class InjectStepCurrentGlomerulus(sciunit.Capability):
    """Enables injecting step current stimulus to glomerulus"""

    def inject_step_current_glomerulus(self, current: dict):
        """Model should implement this method such as to inject the specified
        current stimulus into the glomerulus of the neuron.
        Input current is specified in the form of a dict with keys:
            'delay'     : (value in ms),
            'duration'  : (value in ms),
            'amplitude' : (value in nA)
        Example of current stimulus:
        .. code-block:: python
            current = {'delay'    : 10.0,
                       'duration' : 50.0,
                       'amplitude': 1.0  }
        """
        raise NotImplementedError()
