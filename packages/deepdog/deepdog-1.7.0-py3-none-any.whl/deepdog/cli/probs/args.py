import argparse
import os


def parse_args() -> argparse.Namespace:
	def dir_path(path):
		if os.path.isdir(path):
			return path
		else:
			raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

	parser = argparse.ArgumentParser(
		"probs", description="Calculating probability from finished bayesrun"
	)
	parser.add_argument(
		"--log-file",
		type=str,
		help="A filename for logging to, if not provided will only log to stderr",
		default=None,
	)
	parser.add_argument(
		"--bayesrun-directory",
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
		"--coalesced-keys",
		type=str,
		help="A comma separated list of strings over which to coalesce data. By default coalesce over all fields within model names, ignore file level names",
		default="",
	)
	parser.add_argument(
		"--uncoalesced-outfile",
		type=str,
		help="output filename for uncoalesced data. If not provided, will not be written",
		default=None,
	)
	parser.add_argument(
		"--coalesced-outfile",
		type=str,
		help="output filename for coalesced data. If not provided, will not be written",
		default=None,
	)
	return parser.parse_args()
