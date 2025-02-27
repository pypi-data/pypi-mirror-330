import typing
import re
import dataclasses

MODEL_REGEXES = [
	re.compile(pattern)
	for pattern in [
		r"geom_(?P<xmin>-?\d+)_(?P<xmax>-?\d+)_(?P<ymin>-?\d+)_(?P<ymax>-?\d+)_(?P<zmin>-?\d+)_(?P<zmax>-?\d+)-orientation_(?P<orientation>free|fixedxy|fixedz)-dipole_count_(?P<avg_filled>\d+)_(?P<field_name>\w*)",
		r"geom_(?P<xmin>-?\d+)_(?P<xmax>-?\d+)_(?P<ymin>-?\d+)_(?P<ymax>-?\d+)_(?P<zmin>-?\d+)_(?P<zmax>-?\d+)-magnitude_(?P<log_magnitude>\d*\.?\d+)-orientation_(?P<orientation>free|fixedxy|fixedz)-dipole_count_(?P<avg_filled>\d+)_(?P<field_name>\w*)",
		r"geom_(?P<xmin>-?\d*\.?\d+)_(?P<xmax>-?\d*\.?\d+)_(?P<ymin>-?\d*\.?\d+)_(?P<ymax>-?\d*\.?\d+)_(?P<zmin>-?\d*\.?\d+)_(?P<zmax>-?\d*\.?\d+)-magnitude_(?P<log_magnitude>\d*\.?\d+)-orientation_(?P<orientation>free|fixedxy|fixedz)-dipole_count_(?P<avg_filled>\d+)_(?P<field_name>\w*)",
		r"geom_(?P<xmin>-?\d+)_(?P<xmax>-?\d+)_(?P<ymin>-?\d+)_(?P<ymax>-?\d+)_(?P<zmin>-?\d+)_(?P<zmax>-?\d+)-magnitude_(?P<log_magnitude>-?\d*\.?\d+)-orientation_(?P<orientation>free|fixedxy|fixedz)-dipole_count_(?P<avg_filled>\d+)_(?P<field_name>\w*)",
		r"geom_(?P<xmin>-?\d*\.?\d+)_(?P<xmax>-?\d*\.?\d+)_(?P<ymin>-?\d*\.?\d+)_(?P<ymax>-?\d*\.?\d+)_(?P<zmin>-?\d*\.?\d+)_(?P<zmax>-?\d*\.?\d+)-magnitude_(?P<log_magnitude>-?\d*\.?\d+)-orientation_(?P<orientation>free|fixedxy|fixedz)-dipole_count_(?P<avg_filled>\d+)_(?P<field_name>\w*)",
	]
]


@dataclasses.dataclass
class BayesrunModelResult:
	parsed_model_keys: typing.Dict[str, str]
	success: int
	count: int


@dataclasses.dataclass
class GeneralModelResult:
	parsed_model_keys: typing.Dict[str, str]
	result_dict: typing.Dict[str, str]


class BayesrunColumnParsed:
	"""
	class for parsing a bayesrun while pulling certain special fields out
	"""

	def __init__(self, groupdict: typing.Dict[str, str]):
		self.column_field = groupdict["field_name"]
		self.model_field_dict = {
			k: v for k, v in groupdict.items() if k != "field_name"
		}
		self._groupdict_str = repr(groupdict)

	def __str__(self):
		return f"BayesrunColumnParsed[{self.column_field}: {self.model_field_dict}]"

	def __repr__(self):
		return f"BayesrunColumnParsed({self._groupdict_str})"

	def __eq__(self, other):
		if isinstance(other, BayesrunColumnParsed):
			return (self.column_field == other.column_field) and (
				self.model_field_dict == other.model_field_dict
			)
		return NotImplemented


def _parse_bayesrun_column(
	column: str,
) -> typing.Optional[BayesrunColumnParsed]:
	"""
	Tries one by one all of a predefined list of regexes that I might have used in the past.
	Returns the groupdict for the first match, or None if no match found.
	"""
	for pattern in MODEL_REGEXES:
		match = pattern.match(column)
		if match:
			return BayesrunColumnParsed(match.groupdict())
	else:
		return None


def _batch_iterable_into_chunks(iterable, n=1):
	"""
	utility for batching bayesrun files where columns appear in threes
	"""
	for ndx in range(0, len(iterable), n):
		yield iterable[ndx : min(ndx + n, len(iterable))]


def parse_general_row(
	row: typing.Dict[str, str],
	expected_fields: typing.Sequence[typing.Optional[str]],
) -> typing.Sequence[GeneralModelResult]:
	results = []
	batched_keys = _batch_iterable_into_chunks(list(row.keys()), len(expected_fields))
	for model_keys in batched_keys:
		parsed = [_parse_bayesrun_column(column) for column in model_keys]
		values = [row[column] for column in model_keys]

		result_dict = {}
		parsed_keys = None
		for expected_field, parsed_field, value in zip(expected_fields, parsed, values):
			if expected_field is None:
				continue
			if parsed_field is None:
				raise ValueError(
					f"No viable row found for {expected_field=} in {model_keys=}"
				)
			if parsed_field.column_field != expected_field:
				raise ValueError(
					f"The column {parsed_field.column_field} does not match expected {expected_field}"
				)
			result_dict[expected_field] = value
			if parsed_keys is None:
				parsed_keys = parsed_field.model_field_dict

		if parsed_keys is None:
			raise ValueError(f"Somehow parsed keys is none here, for {row=}")
		results.append(
			GeneralModelResult(parsed_model_keys=parsed_keys, result_dict=result_dict)
		)
	return results


def parse_bayesrun_row(
	row: typing.Dict[str, str],
) -> typing.Sequence[BayesrunModelResult]:

	results = []
	batched_keys = _batch_iterable_into_chunks(list(row.keys()), 3)
	for model_keys in batched_keys:
		parsed = [_parse_bayesrun_column(column) for column in model_keys]
		values = [row[column] for column in model_keys]
		if parsed[0] is None:
			raise ValueError(f"no viable success row found for keys {model_keys}")
		if parsed[1] is None:
			raise ValueError(f"no viable count row found for keys {model_keys}")
		if parsed[0].column_field != "success":
			raise ValueError(f"The column {model_keys[0]} is not a success field")
		if parsed[1].column_field != "count":
			raise ValueError(f"The column {model_keys[1]} is not a count field")
		parsed_keys = parsed[0].model_field_dict
		success = int(values[0])
		count = int(values[1])
		results.append(
			BayesrunModelResult(
				parsed_model_keys=parsed_keys,
				success=success,
				count=count,
			)
		)
	return results
