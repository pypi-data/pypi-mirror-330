import logging
import multiprocessing
import numpy
import pdme.measurement
import pdme.measurement.input_types
import pdme.model
import pdme.subspace_simulation
from typing import Sequence, Tuple, Optional, Callable, Union, List

from dataclasses import dataclass

_logger = logging.getLogger(__name__)


@dataclass
class SubsetSimulationResult:
	probs_list: Sequence[Tuple]
	over_target_cost: Optional[float]
	over_target_likelihood: Optional[float]
	under_target_cost: Optional[float]
	under_target_likelihood: Optional[float]
	lowest_likelihood: Optional[float]
	messages: Sequence[str]


@dataclass
class MultiSubsetSimulationResult:
	child_results: Sequence[SubsetSimulationResult]
	model_name: str
	estimated_likelihood: float
	arithmetic_mean_estimated_likelihood: float
	num_children: int
	num_finished_children: int
	clean_estimate: bool


class SubsetSimulation:
	def __init__(
		self,
		model_name_pair,
		# actual_measurements: Sequence[pdme.measurement.DotMeasurement],
		cost_function: Callable[[numpy.ndarray], numpy.ndarray],
		n_c: int,
		n_s: int,
		m_max: int,
		target_cost: Optional[float] = None,
		level_0_seed: Union[int, Sequence[int]] = 200,
		mcmc_seed: Union[int, Sequence[int]] = 20,
		use_adaptive_steps=True,
		default_phi_step=0.01,
		default_theta_step=0.01,
		default_r_step=0.01,
		default_w_log_step=0.01,
		default_upper_w_log_step=4,
		num_initial_dmc_gens=1,
		keep_probs_list=True,
		dump_last_generation_to_file=False,
		initial_cost_chunk_size=100,
		initial_cost_multiprocess=True,
		cap_core_count: int = 0,  # 0 means cap at num cores - 1
	):
		name, model = model_name_pair
		self.model_name = name
		self.model = model
		_logger.info(f"got model {self.model_name}")

		# dot_inputs = [(meas.r, meas.f) for meas in actual_measurements]
		# self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
		# 	dot_inputs
		# )
		# _logger.debug(f"actual measurements: {actual_measurements}")
		# self.actual_measurement_array = numpy.array([m.v for m in actual_measurements])

		# def cost_function_to_use(dipoles_to_test):
		# 	return pdme.subspace_simulation.proportional_costs_vs_actual_measurement(
		# 		self.dot_inputs_array, self.actual_measurement_array, dipoles_to_test
		# 	)

		self.cost_function_to_use = cost_function

		self.n_c = n_c
		self.n_s = n_s
		self.m_max = m_max

		self.level_0_seed = level_0_seed
		self.mcmc_seed = mcmc_seed

		self.use_adaptive_steps = use_adaptive_steps
		self.default_phi_step = (
			default_phi_step * 1.73
		)  # this is a hack to fix a missing sqrt 3 in the proposal function code.
		self.default_theta_step = default_theta_step
		self.default_r_step = (
			default_r_step * 1.73
		)  # this is a hack to fix a missing sqrt 3 in the proposal function code.
		self.default_w_log_step = (
			default_w_log_step * 1.73
		)  # this is a hack to fix a missing sqrt 3 in the proposal function code.
		self.default_upper_w_log_step = default_upper_w_log_step

		_logger.info("using params:")
		_logger.info(f"\tn_c: {self.n_c}")
		_logger.info(f"\tn_s: {self.n_s}")
		_logger.info(f"\tm: {self.m_max}")
		_logger.info(f"\t{num_initial_dmc_gens=}")
		_logger.info(f"\t{mcmc_seed=}")
		_logger.info(f"\t{level_0_seed=}")
		_logger.info("let's do level 0...")

		self.target_cost = target_cost
		_logger.info(f"will stop at target cost {target_cost}")

		self.keep_probs_list = keep_probs_list
		self.dump_last_generations = dump_last_generation_to_file

		self.initial_cost_chunk_size = initial_cost_chunk_size
		self.initial_cost_multiprocess = initial_cost_multiprocess

		self.cap_core_count = cap_core_count

		self.num_dmc_gens = num_initial_dmc_gens

	def _single_chain_gen(self, args: Tuple):
		threshold_cost, stdevs, rng_seed, (c, s) = args
		rng = numpy.random.default_rng(rng_seed)
		return self.model.get_repeat_counting_mcmc_chain(
			s,
			self.cost_function_to_use,
			self.n_s,
			threshold_cost,
			stdevs,
			initial_cost=c,
			rng_arg=rng,
		)

	def execute(self) -> SubsetSimulationResult:

		probs_list = []

		output_messages = []

		# If we have n_s = 10 and n_c = 100, then our big N = 1000 and p = 1/10
		# The DMC stage would normally generate 1000, then pick the best 100 and start counting prob = p/10.
		# Let's say we want our DMC stage to go down to level 2.
		# Then we need to filter out p^2, so our initial has to be N_0 = N / p = n_c * n_s^2
		initial_dmc_n = self.n_c * (self.n_s**self.num_dmc_gens)
		initial_level = (
			self.num_dmc_gens - 1
		)  # This is perfunctory but let's label it here really explicitly
		_logger.info(f"Generating {initial_dmc_n} for DMC stage")
		sample_dipoles = self.model.get_monte_carlo_dipole_inputs(
			initial_dmc_n,
			-1,
			rng_to_use=numpy.random.default_rng(self.level_0_seed),
		)
		# _logger.debug(sample_dipoles)
		# _logger.debug(sample_dipoles.shape)

		_logger.debug("Finished dipole generation")
		_logger.debug(
			f"Using iterated multiprocessing cost function thing with chunk size {self.initial_cost_chunk_size}"
		)

		# core count etc. logic here
		core_count = multiprocessing.cpu_count() - 1 or 1
		if (self.cap_core_count >= 1) and (self.cap_core_count < core_count):
			core_count = self.cap_core_count
		_logger.info(f"Using {core_count} cores")

		with multiprocessing.Pool(core_count) as pool:

			# Do the initial DMC calculation in a multiprocessing

			chunks = numpy.array_split(
				sample_dipoles,
				range(
					self.initial_cost_chunk_size,
					len(sample_dipoles),
					self.initial_cost_chunk_size,
				),
			)
			if self.initial_cost_multiprocess:
				_logger.debug("Multiprocessing initial costs")
				raw_costs = pool.map(self.cost_function_to_use, chunks)
			else:
				_logger.debug("Single process initial costs")
				raw_costs = []
				for chunk_idx, chunk in enumerate(chunks):
					_logger.debug(f"doing chunk #{chunk_idx}")
					raw_costs.append(self.cost_function_to_use(chunk))
			costs = numpy.concatenate(raw_costs)
			_logger.debug("finished initial dmc cost calculation")
			# _logger.debug(f"costs: {costs}")
			sorted_indexes = costs.argsort()[::-1]

			# _logger.debug(costs[sorted_indexes])
			# _logger.debug(sample_dipoles[sorted_indexes])

			sorted_costs = costs[sorted_indexes]
			sorted_dipoles = sample_dipoles[sorted_indexes]

			all_dipoles = numpy.array(
				[
					pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(samp)
					for samp in sorted_dipoles
				]
			)
			all_chains = list(zip(sorted_costs, all_dipoles))
			for dmc_level in range(initial_level):
				# if initial level is 1, we want to print out what the level 0 threshold would have been?
				_logger.debug(f"Get the pseudo statistics for level {dmc_level}")
				_logger.debug(f"Whole chain has length {len(all_chains)}")
				pseudo_threshold_index = -(
					self.n_c * (self.n_s ** (self.num_dmc_gens - dmc_level - 1))
				)
				_logger.debug(
					f"Have a pseudo_threshold_index of {pseudo_threshold_index}, or {len(all_chains) + pseudo_threshold_index}"
				)
				pseudo_threshold_cost = all_chains[-pseudo_threshold_index][0]
				_logger.info(
					f"Pseudo-level {dmc_level} threshold cost {pseudo_threshold_cost}, at P = (1 / {self.n_s})^{dmc_level + 1}"
				)
				all_chains = all_chains[pseudo_threshold_index:]

			long_mcmc_rng = numpy.random.default_rng(self.mcmc_seed)
			mcmc_rng_seed_sequence = numpy.random.SeedSequence(self.mcmc_seed)

			threshold_cost = all_chains[-self.n_c][0]
			_logger.info(
				f"Finishing DMC threshold cost {threshold_cost} at level {initial_level}, at P = (1 / {self.n_s})^{initial_level + 1}"
			)
			_logger.debug(f"Executing the MCMC with chains of length {len(all_chains)}")

			# Now we move on to the MCMC part of the algorithm

			# This is important, we want to allow some extra initial levels so we need to account for that here!
			for i in range(self.num_dmc_gens, self.m_max):
				_logger.info(f"Starting level {i}")
				next_seeds = all_chains[-self.n_c :]

				if self.dump_last_generations:
					_logger.info("writing out csv file")
					next_dipoles_seed_dipoles = numpy.array([n[1] for n in next_seeds])
					for n in range(self.model.n):
						_logger.info(f"{next_dipoles_seed_dipoles[:, n].shape}")
						numpy.savetxt(
							f"generation_{self.n_c}_{self.n_s}_{i}_dipole_{n}.csv",
							next_dipoles_seed_dipoles[:, n],
							delimiter=",",
						)

					next_seeds_as_array = numpy.array([s for _, s in next_seeds])
					stdevs = self.get_stdevs_from_arrays(next_seeds_as_array)
					_logger.info(f"got stdevs: {stdevs.stdevs}")
					all_long_chains = []
					for seed_index, (c, s) in enumerate(
						next_seeds[:: len(next_seeds) // 20]
					):
						# chain = mcmc(s, threshold_cost, n_s, model, dot_inputs_array, actual_measurement_array, mcmc_rng, curr_cost=c, stdevs=stdevs)
						# until new version gotta do
						_logger.debug(
							f"\t{seed_index}: doing long chain on the next seed"
						)

						long_chain = self.model.get_mcmc_chain(
							s,
							self.cost_function_to_use,
							1000,
							threshold_cost,
							stdevs,
							initial_cost=c,
							rng_arg=long_mcmc_rng,
						)
						for _, chained in long_chain:
							all_long_chains.append(chained)
					all_long_chains_array = numpy.array(all_long_chains)
					for n in range(self.model.n):
						_logger.info(f"{all_long_chains_array[:, n].shape}")
						numpy.savetxt(
							f"long_chain_generation_{self.n_c}_{self.n_s}_{i}_dipole_{n}.csv",
							all_long_chains_array[:, n],
							delimiter=",",
						)

				if self.keep_probs_list:
					for cost_index, cost_chain in enumerate(all_chains[: -self.n_c]):
						probs_list.append(
							(
								(
									(self.n_c * self.n_s - cost_index)
									/ (self.n_c * self.n_s)
								)
								/ (self.n_s ** (i)),
								cost_chain[0],
								i + 1,
							)
						)

				next_seeds_as_array = numpy.array([s for _, s in next_seeds])

				stdevs = self.get_stdevs_from_arrays(next_seeds_as_array)
				_logger.debug(f"got stdevs, begin: {stdevs.stdevs[:10]}")
				_logger.debug("Starting the MCMC")
				all_chains = []

				seeds = mcmc_rng_seed_sequence.spawn(len(next_seeds))
				pool_results = pool.imap_unordered(
					self._single_chain_gen,
					[
						(threshold_cost, stdevs, rng_seed, test_seed)
						for rng_seed, test_seed in zip(seeds, next_seeds)
					],
					chunksize=50,
				)

				# count for ergodicity analysis
				samples_generated = 0
				samples_rejected = 0

				for rejected_count, chain in pool_results:
					for cost, chained in chain:
						try:
							filtered_cost = cost[0]
						except (IndexError, TypeError):
							filtered_cost = cost
						all_chains.append((filtered_cost, chained))

					samples_generated += self.n_s
					samples_rejected += rejected_count

				_logger.debug("finished mcmc")
				_logger.debug(f"{samples_rejected=} out of {samples_generated=}")
				if samples_rejected * 2 > samples_generated:
					reject_ratio = samples_rejected / samples_generated
					rejectionmessage = f"On level {i}, rejected {samples_rejected} out of {samples_generated}, {reject_ratio=} is too high and may indicate ergodicity problems"
					output_messages.append(rejectionmessage)
					_logger.warning(rejectionmessage)
				# _logger.debug(all_chains)

				all_chains.sort(key=lambda c: c[0], reverse=True)
				_logger.debug("finished sorting all_chains")

				threshold_cost = all_chains[-self.n_c][0]
				_logger.info(
					f"current threshold cost: {threshold_cost}, at P = (1 / {self.n_s})^{i + 1}"
				)
				if (self.target_cost is not None) and (
					threshold_cost < self.target_cost
				):
					_logger.info(
						f"got a threshold cost {threshold_cost}, less than {self.target_cost}. will leave early"
					)

					cost_list = [c[0] for c in all_chains]
					over_index = reverse_bisect_right(cost_list, self.target_cost)

					winner = all_chains[over_index][1]
					_logger.info(f"Winner obtained: {winner}")
					shorter_probs_list = []
					for cost_index, cost_chain in enumerate(all_chains):
						if self.keep_probs_list:
							probs_list.append(
								(
									(
										(self.n_c * self.n_s - cost_index)
										/ (self.n_c * self.n_s)
									)
									/ (self.n_s ** (i)),
									cost_chain[0],
									i + 1,
								)
							)
						shorter_probs_list.append(
							(
								cost_chain[0],
								(
									(self.n_c * self.n_s - cost_index)
									/ (self.n_c * self.n_s)
								)
								/ (self.n_s ** (i)),
							)
						)
					# _logger.info(shorter_probs_list)
					result = SubsetSimulationResult(
						probs_list=probs_list,
						over_target_cost=shorter_probs_list[over_index - 1][0],
						over_target_likelihood=shorter_probs_list[over_index - 1][1],
						under_target_cost=shorter_probs_list[over_index][0],
						under_target_likelihood=shorter_probs_list[over_index][1],
						lowest_likelihood=shorter_probs_list[-1][1],
						messages=output_messages,
					)
					return result

				# _logger.debug([c[0] for c in all_chains[-n_c:]])
				_logger.info(f"doing level {i + 1}")

		if self.keep_probs_list:
			for cost_index, cost_chain in enumerate(all_chains):
				probs_list.append(
					(
						((self.n_c * self.n_s - cost_index) / (self.n_c * self.n_s))
						/ (self.n_s ** (self.m_max)),
						cost_chain[0],
						self.m_max + 1,
					)
				)
		threshold_cost = all_chains[-self.n_c][0]
		_logger.info(
			f"final threshold cost: {threshold_cost}, at P = (1 / {self.n_s})^{self.m_max + 1}"
		)
		# for a in all_chains[-10:]:
		# 	_logger.info(a)
		# for prob, prob_cost in probs_list:
		# 	_logger.info(f"\t{prob}: {prob_cost}")
		probs_list.sort(key=lambda c: c[0], reverse=True)

		min_likelihood = ((1) / (self.n_c * self.n_s)) / (self.n_s ** (self.m_max))

		result = SubsetSimulationResult(
			probs_list=probs_list,
			over_target_cost=None,
			over_target_likelihood=None,
			under_target_cost=None,
			under_target_likelihood=None,
			lowest_likelihood=min_likelihood,
			messages=output_messages,
		)
		return result

	def get_stdevs_from_arrays(
		self, array
	) -> pdme.subspace_simulation.MCMCStandardDeviation:
		# stdevs = get_stdevs_from_arrays(next_seeds_as_array, model)
		if self.use_adaptive_steps:

			stdev_array = []
			count = array.shape[1]
			for dipole_index in range(count):
				selected = array[:, dipole_index]
				pxs = selected[:, 0]
				pys = selected[:, 1]
				pzs = selected[:, 2]
				thetas = numpy.arccos(pzs / self.model.pfixed)
				phis = numpy.arctan2(pys, pxs)

				rstdevs = numpy.maximum(
					numpy.std(selected, axis=0)[3:6],
					self.default_r_step / (self.n_s * 10),
				)
				frequency_stdevs = numpy.minimum(
					numpy.maximum(
						numpy.std(numpy.log(selected[:, -1])),
						self.default_w_log_step / (self.n_s * 10),
					),
					self.default_upper_w_log_step,
				)
				stdev_array.append(
					pdme.subspace_simulation.DipoleStandardDeviation(
						p_theta_step=max(
							numpy.std(thetas), self.default_theta_step / (self.n_s * 10)
						),
						p_phi_step=max(
							numpy.std(phis), self.default_phi_step / (self.n_s * 10)
						),
						rx_step=rstdevs[0],
						ry_step=rstdevs[1],
						rz_step=rstdevs[2],
						w_log_step=frequency_stdevs,
					)
				)
		else:
			default_stdev = pdme.subspace_simulation.DipoleStandardDeviation(
				self.default_phi_step,
				self.default_theta_step,
				self.default_r_step,
				self.default_r_step,
				self.default_r_step,
				self.default_w_log_step,
			)
			stdev_array = [default_stdev]
		stdevs = pdme.subspace_simulation.MCMCStandardDeviation(stdev_array)
		return stdevs


class MultiSubsetSimulations:
	def __init__(
		self,
		model_name_pairs: Sequence[Tuple[str, pdme.model.DipoleModel]],
		# actual_measurements: Sequence[pdme.measurement.DotMeasurement],
		cost_function: Callable[[numpy.ndarray], numpy.ndarray],
		num_runs: int,
		n_c: int,
		n_s: int,
		m_max: int,
		target_cost: float,
		num_initial_dmc_gens: int = 1,
		level_0_seed_seed: int = 200,
		mcmc_seed_seed: int = 20,
		use_adaptive_steps=True,
		default_phi_step=0.01,
		default_theta_step=0.01,
		default_r_step=0.01,
		default_w_log_step=0.01,
		default_upper_w_log_step=4,
		initial_cost_chunk_size=100,
		cap_core_count: int = 0,  # 0 means cap at num cores - 1
	):
		self.model_name_pairs = model_name_pairs
		self.cost_function = cost_function
		self.num_runs = num_runs
		self.n_c = n_c
		self.n_s = n_s
		self.m_max = m_max
		self.target_cost = target_cost  # This is not optional here!

		self.num_dmc_gens = num_initial_dmc_gens

		self.level_0_seed_seed = level_0_seed_seed
		self.mcmc_seed_seed = mcmc_seed_seed

		self.use_adaptive_steps = use_adaptive_steps
		self.default_phi_step = default_phi_step
		self.default_theta_step = default_theta_step
		self.default_r_step = default_r_step
		self.default_w_log_step = default_w_log_step
		self.default_upper_w_log_step = default_upper_w_log_step
		self.initial_cost_chunk_size = initial_cost_chunk_size
		self.cap_core_count = cap_core_count

	def execute(self) -> Sequence[MultiSubsetSimulationResult]:
		output: List[MultiSubsetSimulationResult] = []
		for model_index, model_name_pair in enumerate(self.model_name_pairs):
			ss_results = [
				SubsetSimulation(
					model_name_pair,
					self.cost_function,
					self.n_c,
					self.n_s,
					self.m_max,
					self.target_cost,
					num_initial_dmc_gens=self.num_dmc_gens,
					level_0_seed=[model_index, run_index, self.level_0_seed_seed],
					mcmc_seed=[model_index, run_index, self.mcmc_seed_seed],
					use_adaptive_steps=self.use_adaptive_steps,
					default_phi_step=self.default_phi_step,
					default_theta_step=self.default_theta_step,
					default_r_step=self.default_r_step,
					default_w_log_step=self.default_w_log_step,
					default_upper_w_log_step=self.default_upper_w_log_step,
					keep_probs_list=False,
					dump_last_generation_to_file=False,
					initial_cost_chunk_size=self.initial_cost_chunk_size,
					cap_core_count=self.cap_core_count,
				).execute()
				for run_index in range(self.num_runs)
			]
			output.append(coalesce_ss_results(model_name_pair[0], ss_results))
		return output


def coalesce_ss_results(
	model_name: str, results: Sequence[SubsetSimulationResult]
) -> MultiSubsetSimulationResult:

	num_finished = sum(1 for res in results if res.under_target_likelihood is not None)

	estimated_likelihoods = numpy.array(
		[
			res.under_target_likelihood
			if res.under_target_likelihood is not None
			else res.lowest_likelihood
			for res in results
		]
	)

	_logger.info(estimated_likelihoods)
	geometric_mean_estimated_likelihoods = numpy.exp(
		numpy.log(estimated_likelihoods).mean()
	)
	_logger.info(geometric_mean_estimated_likelihoods)
	arithmetic_mean_estimated_likelihoods = estimated_likelihoods.mean()

	result = MultiSubsetSimulationResult(
		child_results=results,
		model_name=model_name,
		estimated_likelihood=geometric_mean_estimated_likelihoods,
		arithmetic_mean_estimated_likelihood=arithmetic_mean_estimated_likelihoods,
		num_children=len(results),
		num_finished_children=num_finished,
		clean_estimate=num_finished == len(results),
	)
	return result


def reverse_bisect_right(a, x, lo=0, hi=None):
	"""Return the index where to insert item x in list a, assuming a is sorted in descending order.

	The return value i is such that all e in a[:i] have e >= x, and all e in
	a[i:] have e < x.  So if x already appears in the list, a.insert(x) will
	insert just after the rightmost x already there.

	Optional args lo (default 0) and hi (default len(a)) bound the
	slice of a to be searched.

	Essentially, the function returns number of elements in a which are >= than x.
	>>> a = [8, 6, 5, 4, 2]
	>>> reverse_bisect_right(a, 5)
	3
	>>> a[:reverse_bisect_right(a, 5)]
	[8, 6, 5]
	"""
	if lo < 0:
		raise ValueError("lo must be non-negative")
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo + hi) // 2
		if x > a[mid]:
			hi = mid
		else:
			lo = mid + 1
	return lo
