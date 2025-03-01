"""Deprecated Results API."""

import warnings


class Results:
    """Deprecated Results API."""

    def __init__(self, **kwargs):  # type: ignore
        """Initialize the Results API.

        Raises:
            DeprecationWarning: Deprecation warning
        """
        msg = """
        CHIME/FRB Results API has been deprecated.

        Possible Resolutions:

        - Migrate to using the Workflow API instead.
            from workflow.http.context import HTTPContext
            ctx = HTTPContext()
            ctx.results.info()

        - Pin chime-frb-api to 3.4.0 in your project's dependencies.
            poetry update chime-frb-api==3.4.0

        For more information, see docs @ https://chimefrb.github.io/workflow-docs/
        """
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)

        raise DeprecationWarning(msg)
