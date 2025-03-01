# encoding: utf-8
"""

"""
__author__ = "Richard Smith"
__date__ = "01 Jun 2021"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "richard.d.smith@stfc.ac.uk"

import logging
from typing import Optional, Union

import pkg_resources
from extraction_methods.core.extraction_method import ExtractionMethod

LOGGER = logging.getLogger(__name__)


class HandlerPicker:
    """Loads the entrypoints

    Attributes:
        handlers - Dictionary of entry points. The dict is structured:

        .. code-block::

            {
                <entry-point-name>: <entry-point>,
                ...
            }
    """

    def __init__(self, entry_point_key: Union[list, str]):
        """
        Entry points to load from in the setup.py

        :param entry_point_key: name of the entry point source
        """
        self.handlers = {}

        if entry_point_key:
            self.handlers = self._get_entrypoints(entry_point_key)

    @staticmethod
    def _get_entrypoints(group) -> dict:
        """
        Get entrypoints for given group

        :param group: The named entry group

        :return: dict of entrypoints
        """
        entry_points = {}

        for entry_point in pkg_resources.iter_entry_points(group):
            entry_points[entry_point.name] = entry_point

        return entry_points

    def get(self, name: str, **kwargs) -> Optional[ExtractionMethod]:
        """
        Get the processor by name

        :param name: The name of the requested processor

        :return: Processor class
        """

        # Get the processor
        entry_point = self.handlers.get(name)

        if not entry_point:
            LOGGER.error("Failed to load processor: %s", name)
            return

        processor = entry_point.load()

        return processor(**kwargs)
