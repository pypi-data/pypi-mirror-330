import logging
import argparse
import json

import deepdog.cli.subset_sim_probs.args
import deepdog.cli.subset_sim_probs.dicts
import deepdog.cli.util
import deepdog.results
import deepdog.indexify
import pathlib
import tqdm
import os
import tqdm.contrib.logging


_logger = logging.getLogger(__name__)


def set_up_logging(log_file: str):

	log_pattern = "%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s"
	if log_file is None:
		handlers = [
			logging.StreamHandler(),
		]
	else:
		handlers = [logging.StreamHandler(), logging.FileHandler(log_file)]
	logging.basicConfig(
		level=logging.DEBUG,
		format=log_pattern,
		# it's okay to ignore this mypy error because who cares about logger handler types
		handlers=handlers,  # type: ignore
	)
	logging.captureWarnings(True)


def main(args: argparse.Namespace):
	"""
	Main function with passed in arguments and no additional logging setup in case we want to extract out later
	"""

	with tqdm.contrib.logging.logging_redirect_tqdm():
		_logger.info(f"args: {args}")

		if "outfile" in args and args.outfile:
			if os.path.exists(args.outfile):
				if args.never_overwrite_outfile:
					_logger.warning(
						f"Filename {args.outfile} already exists, and never want overwrite, so aborting."
					)
					return
				elif args.force_overwrite_outfile:
					_logger.warning(f"Forcing overwrite of {args.outfile}")
				else:
					# need to confirm
					confirm_overwrite = deepdog.cli.util.confirm_prompt(
						f"Filename {args.outfile} exists, overwrite?"
					)
					if not confirm_overwrite:
						_logger.warning(
							f"Filename {args.outfile} already exists and do not want overwrite, aborting."
						)
						return
					else:
						_logger.warning(f"Overwriting file {args.outfile}")

		indexifier = None
		if args.indexify_json:
			with open(args.indexify_json, "r") as indexify_json_file:
				indexify_spec = json.load(indexify_json_file)
				indexify_data = indexify_spec["indexes"]
				if "seed_spec" in indexify_spec:
					seed_spec = indexify_spec["seed_spec"]
					indexify_data[seed_spec["field_name"]] = list(
						range(seed_spec["num_seeds"])
					)
				# _logger.debug(f"Indexifier data looks like {indexify_data}")
				indexifier = deepdog.indexify.Indexifier(indexify_data)

		results_dir = pathlib.Path(args.results_directory)
		out_files = [
			f for f in results_dir.iterdir() if f.name.endswith("subsetsim.csv")
		]
		_logger.info(
			f"Reading {len(out_files)} subsetsim.csv files in directory {args.results_directory}"
		)
		# _logger.info(out_files)
		parsed_output_files = [
			deepdog.results.read_subset_sim_file(f, indexifier)
			for f in tqdm.tqdm(out_files, desc="reading files", leave=False)
		]

		# Refactor here to allow for arbitrary likelihood file sources
		_logger.info("building uncoalesced dict")
		uncoalesced_dict = deepdog.cli.subset_sim_probs.dicts.build_model_dict(
			parsed_output_files
		)

		_logger.info("building coalesced dict")
		coalesced = deepdog.cli.subset_sim_probs.dicts.coalesced_dict(uncoalesced_dict)

		if "outfile" in args and args.outfile:
			deepdog.cli.subset_sim_probs.dicts.write_coalesced_dict(
				args.outfile, coalesced
			)
		else:
			_logger.info("Skipping writing coalesced")


def wrapped_main():
	args = deepdog.cli.subset_sim_probs.args.parse_args()
	set_up_logging(args.log_file)
	main(args)
