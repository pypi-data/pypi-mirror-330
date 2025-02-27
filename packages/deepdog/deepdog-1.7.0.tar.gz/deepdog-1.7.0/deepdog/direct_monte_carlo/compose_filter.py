from typing import Sequence
from deepdog.direct_monte_carlo.direct_mc import DirectMonteCarloFilter
import numpy


class ComposedDMCFilter(DirectMonteCarloFilter):
	def __init__(self, filters: Sequence[DirectMonteCarloFilter]):
		self.filters = filters

	def filter_samples(self, samples: numpy.ndarray) -> numpy.ndarray:
		current_sample = samples
		for filter in self.filters:
			current_sample = filter.filter_samples(current_sample)
		return current_sample
