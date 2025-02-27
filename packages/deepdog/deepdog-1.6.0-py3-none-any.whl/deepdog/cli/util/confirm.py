_RESPONSE_MAP = {
	"yes": True,
	"ye": True,
	"y": True,
	"no": False,
	"n": False,
	"nope": False,
	"true": True,
	"false": False,
}


def confirm_prompt(question: str) -> bool:
	"""Prompt with the question and returns yes or no based on response."""
	prompt = question + " [y/n]: "

	while True:
		choice = input(prompt).lower()

		if choice in _RESPONSE_MAP:
			return _RESPONSE_MAP[choice]
		else:
			print('Respond with "yes" or "no"')
