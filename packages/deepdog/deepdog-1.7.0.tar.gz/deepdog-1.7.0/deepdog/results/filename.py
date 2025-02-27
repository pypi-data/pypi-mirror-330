import re
import typing


FILE_SLUG_REGEXES = [
	re.compile(pattern)
	for pattern in [
		r"(?P<tag>\w+)-(?P<job_index>\d+)",
		r"mock_tarucha-(?P<job_index>\d+)",
		r"(?:(?P<mock>mock)_)?tarucha(?:_(?P<tarucha_run_id>\d+))?-(?P<job_index>\d+)",
		r"(?P<tag>\w+)-(?P<included_dots>[\w,]+)-(?P<target_cost>\d*\.?\d+)-(?P<job_index>\d+)",
	]
]


def parse_file_slug(slug: str) -> typing.Optional[typing.Dict[str, str]]:
	for pattern in FILE_SLUG_REGEXES:
		match = pattern.match(slug)
		if match:
			return match.groupdict()
	else:
		return None
