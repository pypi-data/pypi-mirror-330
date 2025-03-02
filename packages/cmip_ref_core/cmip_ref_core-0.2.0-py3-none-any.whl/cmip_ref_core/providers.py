"""
Interfaces for metrics providers.

This defines how metrics packages interoperate with the REF framework.
"""

from cmip_ref_core.exceptions import InvalidMetricException
from cmip_ref_core.metrics import Metric


def _slugify(value: str) -> str:
    """
    Slugify a string.

    Parameters
    ----------
    value : str
        String to slugify.

    Returns
    -------
    str
        Slugified string.
    """
    return value.lower().replace(" ", "-")


class MetricsProvider:
    """
    Interface for that a metrics provider must implement.

    This provides a consistent interface to multiple different metrics packages.
    """

    def __init__(self, name: str, version: str, slug: str | None = None) -> None:
        self.name = name
        self.slug = slug or _slugify(name)
        self.version = version

        self._metrics: dict[str, Metric] = {}

    def metrics(self) -> list[Metric]:
        """
        Iterate over the available metrics for the provider.

        Returns
        -------
        :
            Iterator over the currently registered metrics.
        """
        return list(self._metrics.values())

    def __len__(self) -> int:
        return len(self._metrics)

    def register(self, metric: Metric) -> None:
        """
        Register a metric with the manager.

        Parameters
        ----------
        metric : Metric
            The metric to register.
        """
        if not isinstance(metric, Metric):
            raise InvalidMetricException(metric, "Metrics must be an instance of the 'Metric' class")
        self._metrics[metric.slug.lower()] = metric

    def get(self, slug: str) -> Metric:
        """
        Get a metric by name.

        Parameters
        ----------
        slug : str
            Name of the metric (case-sensitive).

        Raises
        ------
        KeyError
            If the metric with the given name is not found.

        Returns
        -------
        Metric
            The requested metric.
        """
        return self._metrics[slug.lower()]
