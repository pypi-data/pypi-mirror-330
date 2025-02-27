import pdme.inputs
import pdme.model
import pdme.measurement
import pdme.measurement.input_types
import pdme.measurement.oscillating_dipole
import pdme.util.fast_v_calc
import pdme.util.fast_nonlocal_spectrum
from typing import Sequence, Tuple, List, Dict, Union, Mapping
import datetime
import csv
import multiprocessing
import logging
import numpy


# TODO: remove hardcode
CHUNKSIZE = 50


_logger = logging.getLogger(__name__)


def get_a_result_fast_filter(input) -> int:
	# 								(
	# 	model,
	# 	self.dot_inputs_array_dict,
	# 	low_high_dict,
	# 	self.monte_carlo_count,
	# 	seed,
	# )
	model, dot_inputs_dict, low_high_dict, monte_carlo_count, seed = input

	rng = numpy.random.default_rng(seed)
	# TODO: A long term refactor is to pull the frequency stuff out from here. The None stands for max_frequency, which is unneeded in the actually useful models.
	sample_dipoles = model.get_monte_carlo_dipole_inputs(
		monte_carlo_count, None, rng_to_use=rng
	)

	current_sample = sample_dipoles
	for temp in dot_inputs_dict.keys():
		dot_inputs = dot_inputs_dict[temp]
		lows, highs = low_high_dict[temp]
		for di, low, high in zip(dot_inputs, lows, highs):

			if len(current_sample) < 1:
				break
			vals = pdme.util.fast_v_calc.fast_vs_for_asymmetric_dipoleses(
				numpy.array([di]), current_sample, temp
			)

			current_sample = current_sample[
				numpy.all((vals > low) & (vals < high), axis=1)
			]
	return len(current_sample)


class TempAwareRealSpectrumRun:
	"""
	A bayes run given some real data, with potentially variable temperature.

	Parameters
	----------
	measurements_dict : Dict[float, Sequence[pdme.measurement.DotRangeMeasurement]]
	The dot inputs for this bayes run, in a dictionary indexed by temperatures

	models_with_names : models_with_names: Sequence[Tuple[str, pdme.model.DipoleModel]],

	The models to evaluate.

	actual_model : pdme.model.DipoleModel
	The model which is actually correct.

	filename_slug : str
	The filename slug to include.

	run_count: int
	The number of runs to do.
	"""

	def __init__(
		self,
		measurements_dict: Mapping[
			float, Sequence[pdme.measurement.DotRangeMeasurement]
		],
		models_with_names: Sequence[Tuple[str, pdme.model.DipoleModel]],
		filename_slug: str,
		monte_carlo_count: int = 10000,
		monte_carlo_cycles: int = 10,
		target_success: int = 100,
		max_monte_carlo_cycles_steps: int = 10,
		chunksize: int = CHUNKSIZE,
		initial_seed: int = 12345,
		cap_core_count: int = 0,
	) -> None:
		self.measurements_dict = measurements_dict
		self.dot_inputs_dict = {
			k: [(measure.r, measure.f) for measure in measurements]
			for k, measurements in measurements_dict.items()
		}

		self.dot_inputs_array_dict = {
			k: pdme.measurement.input_types.dot_inputs_to_array(dot_inputs)
			for k, dot_inputs in self.dot_inputs_dict.items()
		}

		self.models = [model for (_, model) in models_with_names]
		self.model_names = [name for (name, _) in models_with_names]
		self.model_count = len(self.models)

		self.monte_carlo_count = monte_carlo_count
		self.monte_carlo_cycles = monte_carlo_cycles
		self.target_success = target_success
		self.max_monte_carlo_cycles_steps = max_monte_carlo_cycles_steps

		self.csv_fields = []

		self.compensate_zeros = True
		self.chunksize = chunksize
		for name in self.model_names:
			self.csv_fields.extend([f"{name}_success", f"{name}_count", f"{name}_prob"])

		# for now initialise priors as uniform.
		self.probabilities = [1 / self.model_count] * self.model_count

		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		ff_string = "fast_filter"
		self.filename = f"{timestamp}-{filename_slug}.realdata.{ff_string}.bayesrun.csv"
		self.initial_seed = initial_seed

		self.cap_core_count = cap_core_count

	def go(self) -> None:
		with open(self.filename, "a", newline="") as outfile:
			writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect="unix")
			writer.writeheader()

		low_high_dict = {}
		for temp, measurements in self.measurements_dict.items():
			(
				lows,
				highs,
			) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
				measurements
			)
			low_high_dict[temp] = (lows, highs)

		# define a new seed sequence for each run
		seed_sequence = numpy.random.SeedSequence(self.initial_seed)

		results = []
		_logger.debug("Going to iterate over models now")
		core_count = multiprocessing.cpu_count() - 1 or 1
		if (self.cap_core_count >= 1) and (self.cap_core_count < core_count):
			core_count = self.cap_core_count
		_logger.info(f"Using {core_count} cores")
		for model_count, (model, model_name) in enumerate(
			zip(self.models, self.model_names)
		):
			_logger.debug(f"Doing model #{model_count}: {model_name}")
			with multiprocessing.Pool(core_count) as pool:
				cycle_count = 0
				cycle_success = 0
				cycles = 0
				while (cycles < self.max_monte_carlo_cycles_steps) and (
					cycle_success <= self.target_success
				):
					_logger.debug(f"Starting cycle {cycles}")
					cycles += 1
					current_success = 0
					cycle_count += self.monte_carlo_count * self.monte_carlo_cycles

					# generate a seed from the sequence for each core.
					# note this needs to be inside the loop for monte carlo cycle steps!
					# that way we get more stuff.
					seeds = seed_sequence.spawn(self.monte_carlo_cycles)

					result_func = get_a_result_fast_filter

					current_success = sum(
						pool.imap_unordered(
							result_func,
							[
								(
									model,
									self.dot_inputs_array_dict,
									low_high_dict,
									self.monte_carlo_count,
									seed,
								)
								for seed in seeds
							],
							self.chunksize,
						)
					)

					cycle_success += current_success
					_logger.debug(f"current running successes: {cycle_success}")
				results.append((cycle_count, cycle_success))

		_logger.debug("Done, constructing output now")
		row: Dict[str, Union[int, float, str]] = {}

		successes: List[float] = []
		counts: List[int] = []
		for model_index, (name, (count, result)) in enumerate(
			zip(self.model_names, results)
		):

			row[f"{name}_success"] = result
			row[f"{name}_count"] = count
			successes.append(max(result, 0.5))
			counts.append(count)

		success_weight = sum(
			[
				(succ / count) * prob
				for succ, count, prob in zip(successes, counts, self.probabilities)
			]
		)
		new_probabilities = [
			(succ / count) * old_prob / success_weight
			for succ, count, old_prob in zip(successes, counts, self.probabilities)
		]
		self.probabilities = new_probabilities
		for name, probability in zip(self.model_names, self.probabilities):
			row[f"{name}_prob"] = probability
		_logger.info(row)

		with open(self.filename, "a", newline="") as outfile:
			writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect="unix")
			writer.writerow(row)
