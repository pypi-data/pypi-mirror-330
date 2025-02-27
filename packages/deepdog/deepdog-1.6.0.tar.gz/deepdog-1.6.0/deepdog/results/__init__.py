import dataclasses
import re
import typing
import logging
import deepdog.indexify
import pathlib
import csv
from deepdog.results.read_csv import (
	parse_bayesrun_row,
	BayesrunModelResult,
	parse_general_row,
	GeneralModelResult,
)
from deepdog.results.filename import parse_file_slug

_logger = logging.getLogger(__name__)

FILENAME_REGEX = re.compile(
	r"(?P<timestamp>\d{8}-\d{6})-(?P<filename_slug>.*)\.realdata\.fast_filter\.bayesrun\.csv"
)

# probably a better way but who cares
NO_TIMESTAMP_FILENAME_REGEX = re.compile(
	r"(?P<filename_slug>.*)\.realdata\.fast_filter\.bayesrun\.csv"
)


SUBSET_SIM_FILENAME_REGEX = re.compile(
	r"(?P<filename_slug>.*)-(?:no_adaptive_steps_)?(?P<num_ss_runs>\d+)-nc_(?P<n_c>\d+)-ns_(?P<n_s>\d+)-mmax_(?P<mmax>\d+)\.multi\.subsetsim\.csv"
)


@dataclasses.dataclass
class BayesrunOutputFilename:
	timestamp: typing.Optional[str]
	filename_slug: str
	path: pathlib.Path


@dataclasses.dataclass
class BayesrunOutput:
	filename: BayesrunOutputFilename
	data: typing.Dict["str", typing.Any]
	results: typing.Sequence[BayesrunModelResult]


@dataclasses.dataclass
class GeneralOutput:
	filename: BayesrunOutputFilename
	data: typing.Dict["str", typing.Any]
	results: typing.Sequence[GeneralModelResult]


def _parse_string_output_filename(
	filename: str,
) -> typing.Tuple[typing.Optional[str], str]:
	if match := FILENAME_REGEX.match(filename):
		groups = match.groupdict()
		return (groups["timestamp"], groups["filename_slug"])
	elif match := NO_TIMESTAMP_FILENAME_REGEX.match(filename):
		groups = match.groupdict()
		return (None, groups["filename_slug"])
	else:
		raise ValueError(f"Could not parse {filename} as a bayesrun output filename")


def _parse_output_filename(file: pathlib.Path) -> BayesrunOutputFilename:
	filename = file.name
	timestamp, slug = _parse_string_output_filename(filename)
	return BayesrunOutputFilename(timestamp=timestamp, filename_slug=slug, path=file)


def _parse_ss_output_filename(file: pathlib.Path) -> BayesrunOutputFilename:
	filename = file.name
	match = SUBSET_SIM_FILENAME_REGEX.match(filename)
	if not match:
		raise ValueError(f"{filename} was not a valid subset sim output")
	groups = match.groupdict()
	return BayesrunOutputFilename(
		filename_slug=groups["filename_slug"], path=file, timestamp=None
	)


def read_subset_sim_file(
	file: pathlib.Path, indexifier: typing.Optional[deepdog.indexify.Indexifier]
) -> GeneralOutput:

	parsed_filename = tag = _parse_ss_output_filename(file)
	out = GeneralOutput(filename=parsed_filename, data={}, results=[])

	out.data.update(dataclasses.asdict(tag))
	parsed_tag = parse_file_slug(parsed_filename.filename_slug)
	if parsed_tag is None:
		_logger.warning(
			f"Could not parse {tag} against any matching regexes. Going to skip tag parsing"
		)
	else:
		out.data.update(parsed_tag)
		if indexifier is not None:
			try:
				job_index = parsed_tag["job_index"]
				indexified = indexifier.indexify(int(job_index))
				out.data.update(indexified)
			except KeyError:
				# This isn't really that important of an error, apart from the warning
				_logger.warning(
					f"Parsed tag to {parsed_tag}, and attempted to indexify but no job_index key was found. skipping and moving on"
				)

	with file.open() as input_file:
		reader = csv.DictReader(input_file)
		rows = [r for r in reader]
		if len(rows) == 1:
			row = rows[0]
		else:
			raise ValueError(f"Confused about having multiple rows in {file.name}")
	results = parse_general_row(
		row, ("num_finished_runs", "num_runs", None, "estimated_likelihood")
	)

	out.results = results

	return out


def read_output_file(
	file: pathlib.Path, indexifier: typing.Optional[deepdog.indexify.Indexifier]
) -> BayesrunOutput:

	parsed_filename = tag = _parse_output_filename(file)
	out = BayesrunOutput(filename=parsed_filename, data={}, results=[])

	out.data.update(dataclasses.asdict(tag))
	parsed_tag = parse_file_slug(parsed_filename.filename_slug)
	if parsed_tag is None:
		_logger.warning(
			f"Could not parse {tag} against any matching regexes. Going to skip tag parsing"
		)
	else:
		out.data.update(parsed_tag)
		if indexifier is not None:
			try:
				job_index = parsed_tag["job_index"]
				indexified = indexifier.indexify(int(job_index))
				out.data.update(indexified)
			except KeyError:
				# This isn't really that important of an error, apart from the warning
				_logger.warning(
					f"Parsed tag to {parsed_tag}, and attempted to indexify but no job_index key was found. skipping and moving on"
				)

	with file.open() as input_file:
		reader = csv.DictReader(input_file)
		rows = [r for r in reader]
		if len(rows) == 1:
			row = rows[0]
		else:
			raise ValueError(f"Confused about having multiple rows in {file.name}")
	results = parse_bayesrun_row(row)

	out.results = results

	return out


__all__ = ["read_output_file", "BayesrunOutput"]
