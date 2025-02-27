import csv
import pdme.model
import pdme.measurement
import pdme.measurement.input_types
import pdme.subspace_simulation
import datetime
from typing import Tuple, Dict, NewType, Any, Sequence
from dataclasses import dataclass
import logging
import numpy
import numpy.random
import pdme.util.fast_v_calc
import multiprocessing

_logger = logging.getLogger(__name__)

ANTI_ZERO_SUCCESS_THRES = 0.1


@dataclass
class DirectMonteCarloResult:
	successes: int
	monte_carlo_count: int
	likelihood: float
	model_name: str


@dataclass
class DirectMonteCarloConfig:
	monte_carlo_count_per_cycle: int = 10000
	monte_carlo_cycles: int = 10
	target_success: int = 100
	max_monte_carlo_cycles_steps: int = 10
	monte_carlo_seed: int = 1234
	write_successes_to_file: bool = False
	tag: str = ""
	cap_core_count: int = 0  # 0 means cap at num cores - 1
	chunk_size: int = 50
	write_bayesrun_file: bool = True
	bayesrun_file_timestamp: bool = True
	# chunk size of some kind


# Aliasing dict as a generic data container
DirectMonteCarloData = NewType("DirectMonteCarloData", Dict[str, Any])


class DirectMonteCarloFilter:
	"""
	Abstract class for filtering out samples matching some criteria. Initialise with data as needed,
	then filter out samples as needed.
	"""

	def filter_samples(self, samples: numpy.ndarray) -> numpy.ndarray:
		raise NotImplementedError


class DirectMonteCarloRun:
	"""
	A single model Direct Monte Carlo run, currently implemented only using single threading.
	An encapsulation of the steps needed for a Bayes run.

	Parameters
	----------
	model_name_pairs : Sequence[Tuple(str, pdme.model.DipoleModel)]
	The models to evaluate, with names

	measurements: Sequence[pdme.measurement.DotRangeMeasurement]
	The measurements as dot ranges to use as the bounds for the Monte Carlo calculation.

	monte_carlo_count_per_cycle: int
	The number of Monte Carlo iterations to use in a single cycle calculation.

	monte_carlo_cycles: int
	The number of cycles to use in each step.
	Increasing monte_carlo_count_per_cycle increases memory usage (and runtime), while this increases runtime, allowing
	control over memory use.

	target_success: int
	The number of successes to target before exiting early.
	Should likely be ~100 but can go higher to.

	max_monte_carlo_cycles_steps: int
	The number of steps to use. Each step consists of monte_carlo_cycles cycles, each of which has monte_carlo_count_per_cycle iterations.

	monte_carlo_seed: int
	The seed to use for the RNG.
	"""

	def __init__(
		self,
		model_name_pairs: Sequence[Tuple[str, pdme.model.DipoleModel]],
		filter: DirectMonteCarloFilter,
		config: DirectMonteCarloConfig,
	):
		self.model_name_pairs = model_name_pairs

		# self.measurements = measurements
		# self.dot_inputs = [(measure.r, measure.f) for measure in self.measurements]

		# self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
		# 	self.dot_inputs
		# )

		self.config = config
		self.filter = filter
		# (
		# 	self.lows,
		# 	self.highs,
		# ) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
		# 	self.measurements
		# )

	def _single_run(
		self, model_name_pair: Tuple[str, pdme.model.DipoleModel], seed
	) -> numpy.ndarray:
		rng = numpy.random.default_rng(seed)

		_, model = model_name_pair
		# don't log here it's madness
		# _logger.info(f"Executing for model {model_name}")

		sample_dipoles = model.get_monte_carlo_dipole_inputs(
			self.config.monte_carlo_count_per_cycle, -1, rng
		)

		current_sample = sample_dipoles

		return self.filter.filter_samples(current_sample)
		# for di, low, high in zip(self.dot_inputs_array, self.lows, self.highs):

		# 	if len(current_sample) < 1:
		# 		break
		# 	vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
		# 		numpy.array([di]), current_sample
		# 	)

		# 	current_sample = current_sample[
		# 		numpy.all((vals > low) & (vals < high), axis=1)
		# 	]
		# return current_sample

	def _wrapped_single_run(self, args: Tuple):
		"""
		single run wrapped up for multiprocessing call.

		takes in a tuple of arguments corresponding to
		(model_name_pair, seed, return_configs)

		return_configs is a boolean, if true then will return tuple of (count, [matching configs])
		if false, return (count, [])
		"""
		# here's where we do our work

		model_name_pair, seed, return_configs = args
		cycle_success_configs = self._single_run(model_name_pair, seed)
		cycle_success_count = len(cycle_success_configs)

		if return_configs:
			return (cycle_success_count, cycle_success_configs)
		else:
			return (cycle_success_count, [])

	def execute_no_multiprocessing(self) -> Sequence[DirectMonteCarloResult]:

		count_per_step = (
			self.config.monte_carlo_count_per_cycle * self.config.monte_carlo_cycles
		)
		seed_sequence = numpy.random.SeedSequence(self.config.monte_carlo_seed)

		# core count etc. logic here

		results = []
		for model_name_pair in self.model_name_pairs:
			step_count = 0
			total_success = 0
			total_count = 0

			_logger.info(f"Working on model {model_name_pair[0]}")
			# This is probably where multiprocessing logic should go
			while (step_count < self.config.max_monte_carlo_cycles_steps) and (
				total_success < self.config.target_success
			):
				_logger.debug(f"Executing step {step_count}")
				for cycle_i, seed in enumerate(
					seed_sequence.spawn(self.config.monte_carlo_cycles)
				):
					# here's where we do our work
					cycle_success_configs = self._single_run(model_name_pair, seed)
					cycle_success_count = len(cycle_success_configs)
					if cycle_success_count > 0:
						_logger.debug(
							f"For cycle {cycle_i} received {cycle_success_count} successes"
						)
						# _logger.debug(cycle_success_configs)
						if self.config.write_successes_to_file:
							sorted_by_freq = numpy.array(
								[
									pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(
										dipole_config
									)
									for dipole_config in cycle_success_configs
								]
							)
							dipole_count = numpy.array(cycle_success_configs).shape[1]
							for n in range(dipole_count):
								number_dipoles_to_write = self.config.target_success * 5
								_logger.info(f"Limiting to {number_dipoles_to_write=}")
								numpy.savetxt(
									f"{self.config.tag}_{step_count}_{cycle_i}_dipole_{n}.csv",
									sorted_by_freq[:number_dipoles_to_write, n],
									delimiter=",",
								)
					total_success += cycle_success_count
				_logger.debug(
					f"At end of step {step_count} have {total_success} successes"
				)
				step_count += 1
				total_count += count_per_step

			results.append(
				DirectMonteCarloResult(
					successes=total_success,
					monte_carlo_count=total_count,
					likelihood=total_success / total_count,
					model_name=model_name_pair[0],
				)
			)
		return results

	def execute(self) -> Sequence[DirectMonteCarloResult]:

		# set starting execution timestamp
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

		count_per_step = (
			self.config.monte_carlo_count_per_cycle * self.config.monte_carlo_cycles
		)
		seed_sequence = numpy.random.SeedSequence(self.config.monte_carlo_seed)

		# core count etc. logic here
		core_count = multiprocessing.cpu_count() - 1 or 1
		if (self.config.cap_core_count >= 1) and (
			self.config.cap_core_count < core_count
		):
			core_count = self.config.cap_core_count
		_logger.info(f"Using {core_count} cores")

		results = []
		with multiprocessing.Pool(core_count) as pool:

			for model_name_pair in self.model_name_pairs:
				_logger.info(f"Working on model {model_name_pair[0]}")
				# This is probably where multiprocessing logic should go

				step_count = 0
				total_success = 0
				total_count = 0

				while (step_count < self.config.max_monte_carlo_cycles_steps) and (
					total_success < self.config.target_success
				):

					step_count += 1

					_logger.debug(f"Executing step {step_count}")

					seeds = seed_sequence.spawn(self.config.monte_carlo_cycles)

					raw_pool_results = list(
						pool.imap_unordered(
							self._wrapped_single_run,
							[
								(
									model_name_pair,
									seed,
									self.config.write_successes_to_file,
								)
								for seed in seeds
							],
							self.config.chunk_size,
						)
					)

					pool_results = sum(result[0] for result in raw_pool_results)

					_logger.debug(f"Pool results: {pool_results}")

					if self.config.write_successes_to_file:

						_logger.info("Writing dipole results")

						cycle_success_configs = numpy.concatenate(
							[result[1] for result in raw_pool_results]
						)

						dipole_count = numpy.array(cycle_success_configs).shape[1]

						max_number_dipoles_to_write = self.config.target_success * 5
						_logger.debug(
							f"Limiting to {max_number_dipoles_to_write=}, have {len(cycle_success_configs)}"
						)

						if len(cycle_success_configs):
							sorted_by_freq = numpy.array(
								[
									pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(
										dipole_config
									)
									for dipole_config in cycle_success_configs[
										:max_number_dipoles_to_write
									]
								]
							)

							for n in range(dipole_count):

								dipole_filename = (
									f"{self.config.tag}_{step_count}_dipole_{n}.csv"
								)
								_logger.debug(
									f"Writing {min(len(cycle_success_configs), max_number_dipoles_to_write)} to {dipole_filename}"
								)

								numpy.savetxt(
									dipole_filename,
									sorted_by_freq[:, n],
									delimiter=",",
								)
						else:
							_logger.debug(
								"Instructed to write results, but none obtained"
							)

					total_success += pool_results
					total_count += count_per_step
					_logger.debug(
						f"At end of step {step_count} have {total_success} successes"
					)

				results.append(
					DirectMonteCarloResult(
						successes=total_success,
						monte_carlo_count=total_count,
						likelihood=total_success / total_count,
						model_name=model_name_pair[0],
					)
				)

		if self.config.write_bayesrun_file:

			if self.config.bayesrun_file_timestamp:
				timestamp_str = f"{timestamp}-"
			else:
				timestamp_str = ""
			filename = (
				f"{timestamp_str}{self.config.tag}.realdata.fast_filter.bayesrun.csv"
			)

			_logger.info(f"Going to write to file [{filename}]")
			# row: Dict[str, Union[int, float, str]] = {}
			row = {}

			num_models = len(self.model_name_pairs)
			success_weight = sum(
				[
					(
						max(ANTI_ZERO_SUCCESS_THRES, res.successes)
						/ res.monte_carlo_count
					)
					/ num_models
					for res in results
				]
			)

			for res in results:
				row.update(
					{
						f"{res.model_name}_success": res.successes,
						f"{res.model_name}_count": res.monte_carlo_count,
						f"{res.model_name}_prob": (
							max(ANTI_ZERO_SUCCESS_THRES, res.successes)
							/ res.monte_carlo_count
						)
						/ (num_models * success_weight),
					}
				)
			_logger.info(f"Writing row {row}")
			fieldnames = list(row.keys())

			with open(filename, "w", newline="") as outfile:
				writer = csv.DictWriter(outfile, fieldnames=fieldnames, dialect="unix")
				writer.writeheader()
				writer.writerow(row)

		return results
