import pdme.inputs
import pdme.model
import pdme.measurement
import pdme.measurement.input_types
import pdme.measurement.oscillating_dipole
import pdme.util.fast_v_calc
import pdme.util.fast_nonlocal_spectrum
from typing import Sequence, Tuple, List, Dict, Union, Optional
import datetime
import csv
import multiprocessing
import logging
import numpy


# TODO: remove hardcode
CHUNKSIZE = 50


_logger = logging.getLogger(__name__)


def get_a_result_fast_filter_pairs(input) -> int:
	(
		model,
		dot_inputs,
		lows,
		highs,
		pair_inputs,
		pair_lows,
		pair_highs,
		monte_carlo_count,
		seed,
	) = input

	rng = numpy.random.default_rng(seed)
	# TODO: A long term refactor is to pull the frequency stuff out from here. The None stands for max_frequency, which is unneeded in the actually useful models.
	sample_dipoles = model.get_monte_carlo_dipole_inputs(
		monte_carlo_count, None, rng_to_use=rng
	)

	current_sample = sample_dipoles
	for di, low, high in zip(dot_inputs, lows, highs):

		if len(current_sample) < 1:
			break
		vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
			numpy.array([di]), current_sample
		)

		current_sample = current_sample[numpy.all((vals > low) & (vals < high), axis=1)]

	for pi, plow, phigh in zip(pair_inputs, pair_lows, pair_highs):
		if len(current_sample) < 1:
			break
		vals = pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(
			numpy.array([pi]), current_sample
		)

		current_sample = current_sample[
			numpy.all(
				((vals > plow) & (vals < phigh)) | ((vals < plow) & (vals > phigh)),
				axis=1,
			)
		]
	return len(current_sample)


def get_a_result_fast_filter_potential_pair_phase_only(input) -> int:
	(
		model,
		pair_inputs,
		pair_phase_lows,
		pair_phase_highs,
		monte_carlo_count,
		seed,
	) = input

	rng = numpy.random.default_rng(seed)
	# TODO: A long term refactor is to pull the frequency stuff out from here. The None stands for max_frequency, which is unneeded in the actually useful models.
	sample_dipoles = model.get_monte_carlo_dipole_inputs(
		monte_carlo_count, None, rng_to_use=rng
	)

	current_sample = sample_dipoles

	for pi, plow, phigh in zip(pair_inputs, pair_phase_lows, pair_phase_highs):
		if len(current_sample) < 1:
			break
		vals = pdme.util.fast_nonlocal_spectrum.signarg(
			pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(
				numpy.array([pi]), current_sample
			)
		)

		current_sample = current_sample[
			numpy.all(
				((vals > plow) & (vals < phigh)) | ((vals < plow) & (vals > phigh)),
				axis=1,
			)
		]
	return len(current_sample)


def get_a_result_fast_filter_tarucha_spin_qubit_pair_phase_only(input) -> int:
	(
		model,
		pair_inputs,
		pair_phase_lows,
		pair_phase_highs,
		monte_carlo_count,
		seed,
	) = input

	rng = numpy.random.default_rng(seed)
	# TODO: A long term refactor is to pull the frequency stuff out from here. The None stands for max_frequency, which is unneeded in the actually useful models.
	sample_dipoles = model.get_monte_carlo_dipole_inputs(
		monte_carlo_count, None, rng_to_use=rng
	)

	current_sample = sample_dipoles

	for pi, plow, phigh in zip(pair_inputs, pair_phase_lows, pair_phase_highs):
		if len(current_sample) < 1:
			break

		###
		# This should be  abstracted out, but we're going to dump it here for time pressure's sake
		###
		# vals = pdme.util.fast_nonlocal_spectrum.signarg(
		# 	pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal_dipoleses(
		# 		numpy.array([pi]), current_sample
		# 	)
		#
		vals = pdme.util.fast_nonlocal_spectrum.signarg(
			pdme.util.fast_nonlocal_spectrum.fast_s_spin_qubit_tarucha_nonlocal_dipoleses(
				numpy.array([pi]), current_sample
			)
		)
		current_sample = current_sample[
			numpy.all(
				((vals > plow) & (vals < phigh)) | ((vals < plow) & (vals > phigh)),
				axis=1,
			)
		]
	return len(current_sample)


def get_a_result_fast_filter(input) -> int:
	model, dot_inputs, lows, highs, monte_carlo_count, seed = input

	rng = numpy.random.default_rng(seed)
	# TODO: A long term refactor is to pull the frequency stuff out from here. The None stands for max_frequency, which is unneeded in the actually useful models.
	sample_dipoles = model.get_monte_carlo_dipole_inputs(
		monte_carlo_count, None, rng_to_use=rng
	)

	current_sample = sample_dipoles
	for di, low, high in zip(dot_inputs, lows, highs):

		if len(current_sample) < 1:
			break
		vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
			numpy.array([di]), current_sample
		)

		current_sample = current_sample[numpy.all((vals > low) & (vals < high), axis=1)]
	return len(current_sample)


class RealSpectrumRun:
	"""
	A bayes run given some real data.

	Parameters
	----------
	measurements : Sequence[pdme.measurement.DotRangeMeasurement]
	The dot inputs for this bayes run.

	models_with_names : Sequence[Tuple(str, pdme.model.DipoleModel)]
	The models to evaluate.

	actual_model : pdme.model.DipoleModel
	The model which is actually correct.

	filename_slug : str
	The filename slug to include.

	run_count: int
	The number of runs to do.

	If pair_measurements is not None, uses pair measurement method (and single measurements too).
	If pair_phase_measurements is not None, ignores measurements and uses phase measurements _only_
	This is lazy design on my part.

	"""

	def __init__(
		self,
		measurements: Sequence[pdme.measurement.DotRangeMeasurement],
		models_with_names: Sequence[Tuple[str, pdme.model.DipoleModel]],
		filename_slug: str,
		monte_carlo_count: int = 10000,
		monte_carlo_cycles: int = 10,
		target_success: int = 100,
		max_monte_carlo_cycles_steps: int = 10,
		chunksize: int = CHUNKSIZE,
		initial_seed: int = 12345,
		cap_core_count: int = 0,
		pair_measurements: Optional[
			Sequence[pdme.measurement.DotPairRangeMeasurement]
		] = None,
		pair_phase_measurements: Optional[
			Sequence[pdme.measurement.DotPairRangeMeasurement]
		] = None,
	) -> None:
		self.measurements = measurements
		self.dot_inputs = [(measure.r, measure.f) for measure in self.measurements]

		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
			self.dot_inputs
		)

		if pair_measurements is not None:
			self.pair_measurements = pair_measurements
			self.use_pair_measurements = True
			self.use_pair_phase_measurements = False

			self.dot_pair_inputs = [
				(measure.r1, measure.r2, measure.f)
				for measure in self.pair_measurements
			]
			self.dot_pair_inputs_array = (
				pdme.measurement.input_types.dot_pair_inputs_to_array(
					self.dot_pair_inputs
				)
			)
		elif pair_phase_measurements is not None:
			self.use_pair_measurements = False
			self.use_pair_phase_measurements = True
			self.pair_phase_measurements = pair_phase_measurements
			self.dot_pair_inputs = [
				(measure.r1, measure.r2, measure.f)
				for measure in self.pair_phase_measurements
			]
			self.dot_pair_inputs_array = (
				pdme.measurement.input_types.dot_pair_inputs_to_array(
					self.dot_pair_inputs
				)
			)
		else:
			self.use_pair_measurements = False
			self.use_pair_phase_measurements = False

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

		(
			lows,
			highs,
		) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
			self.measurements
		)

		pair_lows = None
		pair_highs = None
		if self.use_pair_measurements:
			(
				pair_lows,
				pair_highs,
			) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
				self.pair_measurements
			)

		pair_phase_lows = None
		pair_phase_highs = None
		if self.use_pair_phase_measurements:
			(
				pair_phase_lows,
				pair_phase_highs,
			) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
				self.pair_phase_measurements
			)

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

					if self.use_pair_measurements:
						_logger.debug("using pair measurements")
						current_success = sum(
							pool.imap_unordered(
								get_a_result_fast_filter_pairs,
								[
									(
										model,
										self.dot_inputs_array,
										lows,
										highs,
										self.dot_pair_inputs_array,
										pair_lows,
										pair_highs,
										self.monte_carlo_count,
										seed,
									)
									for seed in seeds
								],
								self.chunksize,
							)
						)
					elif self.use_pair_phase_measurements:
						_logger.debug("using pair phase measurements")
						_logger.debug("specifically using tarucha")
						current_success = sum(
							pool.imap_unordered(
								get_a_result_fast_filter_tarucha_spin_qubit_pair_phase_only,
								[
									(
										model,
										self.dot_pair_inputs_array,
										pair_phase_lows,
										pair_phase_highs,
										self.monte_carlo_count,
										seed,
									)
									for seed in seeds
								],
								self.chunksize,
							)
						)
					else:

						current_success = sum(
							pool.imap_unordered(
								get_a_result_fast_filter,
								[
									(
										model,
										self.dot_inputs_array,
										lows,
										highs,
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
