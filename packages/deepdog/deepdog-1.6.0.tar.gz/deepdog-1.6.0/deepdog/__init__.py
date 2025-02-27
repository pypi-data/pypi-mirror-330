import logging
from deepdog.meta import __version__
from deepdog.real_spectrum_run import RealSpectrumRun
from deepdog.temp_aware_real_spectrum_run import TempAwareRealSpectrumRun


def get_version():
	return __version__


__all__ = [
	"get_version",
	"RealSpectrumRun",
	"TempAwareRealSpectrumRun",
]


logging.getLogger(__name__).addHandler(logging.NullHandler())
