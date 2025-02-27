import typing
from deepdog.results import GeneralOutput
import logging
import csv
import tqdm

_logger = logging.getLogger(__name__)


def build_model_dict(
	general_outputs: typing.Sequence[GeneralOutput],
) -> typing.Dict[
	typing.Tuple, typing.Dict[typing.Tuple, typing.Dict["str", typing.Any]]
]:
	"""
	Maybe someday do something smarter with the coalescing and stuff but don't want to so i won't
	"""
	# assume that everything is well formatted and the keys are the same across entire list and initialise list of keys.
	# model dict will contain a model_key: {calculation_dict} where each calculation_dict represents a single calculation for that model,
	# the uncoalesced version, keyed by the specific file keys
	model_dict: typing.Dict[
		typing.Tuple, typing.Dict[typing.Tuple, typing.Dict["str", typing.Any]]
	] = {}

	_logger.info("building model dict")
	for out in tqdm.tqdm(general_outputs, desc="reading outputs", leave=False):
		for model_result in out.results:
			model_key = tuple(v for v in model_result.parsed_model_keys.values())
			if model_key not in model_dict:
				model_dict[model_key] = {}
			calculation_dict = model_dict[model_key]
			calculation_key = tuple(v for v in out.data.values())
			if calculation_key not in calculation_dict:
				calculation_dict[calculation_key] = {
					"_model_key_dict": model_result.parsed_model_keys,
					"_calculation_key_dict": out.data,
					"num_finished_runs": int(
						model_result.result_dict["num_finished_runs"]
					),
					"num_runs": int(model_result.result_dict["num_runs"]),
					"estimated_likelihood": float(
						model_result.result_dict["estimated_likelihood"]
					),
				}
			else:
				raise ValueError(
					f"Got {calculation_key} twice for model_key {model_key}"
				)

	return model_dict


def coalesced_dict(
	uncoalesced_model_dict: typing.Dict[
		typing.Tuple, typing.Dict[typing.Tuple, typing.Dict["str", typing.Any]]
	],
):
	"""
	pass in uncoalesced dict
	the minimum_count field is what we use to make sure our probs are never zero
	"""
	coalesced_dict = {}

	# we are already iterating so for no reason because performance really doesn't matter let's count the keys ourselves
	num_keys = 0

	# first pass coalesce
	for model_key, model_dict in uncoalesced_model_dict.items():
		num_keys += 1
		for calculation in model_dict.values():
			if model_key not in coalesced_dict:
				coalesced_dict[model_key] = {
					"_model_key_dict": calculation["_model_key_dict"].copy(),
					"calculations_coalesced": 1,
					"num_finished_runs": calculation["num_finished_runs"],
					"num_runs": calculation["num_runs"],
					"estimated_likelihood": calculation["estimated_likelihood"],
				}
			else:
				_logger.error(f"We shouldn't be here! Double key for {model_key=}")
				raise ValueError()

	# second pass do probability calculation

	prior = 1 / num_keys
	_logger.info(f"Got {num_keys} model keys, so our prior will be {prior}")

	total_weight = 0
	for coalesced_model_dict in coalesced_dict.values():
		model_weight = coalesced_model_dict["estimated_likelihood"] * prior
		total_weight += model_weight

	total_prob = 0
	for coalesced_model_dict in coalesced_dict.values():
		likelihood = coalesced_model_dict["estimated_likelihood"]
		prob = likelihood * prior / total_weight
		coalesced_model_dict["prob"] = prob
		total_prob += prob

	_logger.debug(
		f"Got a total probability of {total_prob}, which should be close to 1 up to float/rounding error"
	)
	return coalesced_dict


def write_coalesced_dict(
	coalesced_output_filename: typing.Optional[str],
	coalesced_model_dict: typing.Dict[typing.Tuple, typing.Dict["str", typing.Any]],
):
	if coalesced_output_filename is None or coalesced_output_filename == "":
		_logger.warning("Not provided a uncoalesced filename, not going to try")
		return

	first_value = next(iter(coalesced_model_dict.values()))
	model_field_names = set(first_value["_model_key_dict"].keys())
	_logger.info(f"Detected model field names {model_field_names}")

	collected_fieldnames = list(model_field_names)
	collected_fieldnames.extend(
		["calculations_coalesced", "num_finished_runs", "num_runs", "prob"]
	)
	with open(coalesced_output_filename, "w", newline="") as coalesced_output_file:
		writer = csv.DictWriter(coalesced_output_file, fieldnames=collected_fieldnames)
		writer.writeheader()

		for model_dict in coalesced_model_dict.values():
			row = model_dict["_model_key_dict"].copy()
			row.update(
				{
					"calculations_coalesced": model_dict["calculations_coalesced"],
					"num_finished_runs": model_dict["num_finished_runs"],
					"num_runs": model_dict["num_runs"],
					"prob": model_dict["prob"],
				}
			)
			writer.writerow(row)
