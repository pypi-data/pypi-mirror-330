"""
Probably should just include a way to handle the indexify function I reuse so much.

All about breaking an integer into a tuple of values from lists, which is useful because of how we do CHTC runs.
"""
import itertools
import typing
import logging
import math

_logger = logging.getLogger(__name__)


# from https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
def _dict_product(dicts):
	"""
	>>> list(dict_product(dict(number=[1,2], character='ab')))
	[{'character': 'a', 'number': 1},
	{'character': 'a', 'number': 2},
	{'character': 'b', 'number': 1},
	{'character': 'b', 'number': 2}]
	"""
	return list(dict(zip(dicts.keys(), x)) for x in itertools.product(*dicts.values()))


class Indexifier:
	"""
	The order of keys is very important, but collections.OrderedDict is no longer needed in python 3.7.
	I think it's okay to rely on that.
	"""

	def __init__(self, list_dict: typing.Dict[str, typing.Sequence]):
		self.dict = list_dict
		self.product_dict = _dict_product(self.dict)

	def indexify(self, n: int) -> typing.Dict[str, typing.Any]:
		return self.product_dict[n]

	def __len__(self) -> int:
		weights = [len(v) for v in self.dict.values()]
		return math.prod(weights)

	def _indexify_indices(self, n: int) -> typing.Sequence[int]:
		"""
		legacy indexify from old scripts, copypast.
		could be used like
		>>> ret = {}
		>>> for k, i in zip(self.dict.keys(), self._indexify_indices):
		>>>		ret[k] = self.dict[k][i]
		>>> return ret
		"""
		weights = [len(v) for v in self.dict.values()]
		N = math.prod(weights)
		curr_n = n
		curr_N = N
		out = []
		for w in weights[:-1]:
			# print(f"current: {curr_N}, {curr_n}, {curr_n // w}")
			curr_N = curr_N // w  # should be int division anyway
			out.append(curr_n // curr_N)
			curr_n = curr_n % curr_N
		return out
