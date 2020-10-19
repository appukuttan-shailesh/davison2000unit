import math
import sciunit.scores
import numpy as np

class RMSscore(sciunit.scores.Score):
    """A root mean square score."""

    _allowed_types = (float,)

    _description = (' ',)

    @classmethod
    def compute(cls, observation, prediction):
        """Compute whether the observation equals the prediction."""
        # check for any 'nan' values in the prediction
        for val in prediction:
            if math.isnan(val):
                # if 'nan' in prediction, return 'nan' as score
                return RMSscore(float('nan'))
        rmse = np.sqrt(np.mean((np.array(observation) - np.array(prediction))**2))
        return RMSscore(rmse)

    def __str__(self):
        return '%.3g' % self.score
