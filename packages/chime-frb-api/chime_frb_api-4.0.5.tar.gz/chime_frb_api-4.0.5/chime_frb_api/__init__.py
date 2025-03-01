#!/usr/bin/env python
from pkg_resources import get_distribution as _get_distribution

from chime_frb_api.backends import bucket, distributor, frb_master  # noqa
from chime_frb_api.core.logger import get_logger  # noqa

__version__ = _get_distribution("chime_frb_api").version
