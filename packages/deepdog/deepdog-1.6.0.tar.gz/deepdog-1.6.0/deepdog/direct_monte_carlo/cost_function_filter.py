from deepdog.direct_monte_carlo.direct_mc import DirectMonteCarloFilter
from typing import Callable
import numpy


class CostFunctionTargetFilter(DirectMonteCarloFilter):
	def __init__(
		self,
		cost_function: Callable[[numpy.ndarray], numpy.ndarray],
		target_cost: float,
	):
		"""
		Filters dipoles by cost, only leaving dipoles with cost below target_cost
		"""
		self.cost_function = cost_function
		self.target_cost = target_cost

	def filter_samples(self, samples: numpy.ndarray) -> numpy.ndarray:
		current_sample = samples

		costs = self.cost_function(current_sample)

		current_sample = current_sample[costs < self.target_cost]
		return current_sample
