import argparse
import os


def parse_args() -> argparse.Namespace:
	def dir_path(path):
		if os.path.isdir(path):
			return path
		else:
			raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

	parser = argparse.ArgumentParser(
		"subset_sim_probs",
		description="Calculating probability from finished subset sim run",
	)
	parser.add_argument(
		"--log-file",
		type=str,
		help="A filename for logging to, if not provided will only log to stderr",
		default=None,
	)
	parser.add_argument(
		"--results-directory",
		"-d",
		type=dir_path,
		help="The directory to search for bayesrun files, defaulting to cwd if not passed",
		default=".",
	)
	parser.add_argument(
		"--indexify-json",
		help="A json file with the indexify config for parsing job indexes. Will skip if not present",
		default="",
	)
	parser.add_argument(
		"--outfile",
		"-o",
		type=str,
		help="output filename for coalesced data. If not provided, will not be written",
		default=None,
	)
	confirm_outfile_overwrite_group = parser.add_mutually_exclusive_group()
	confirm_outfile_overwrite_group.add_argument(
		"--never-overwrite-outfile",
		action="store_true",
		help="If a duplicate outfile is detected, skip confirmation and automatically exit early",
	)
	confirm_outfile_overwrite_group.add_argument(
		"--force-overwrite-outfile",
		action="store_true",
		help="Skips checking for duplicate outfiles and overwrites",
	)
	return parser.parse_args()
