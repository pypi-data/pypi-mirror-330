import random
import logging
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


def random_selection(options: list, num_values: int = 1, exclude_options=None):
    # Handle exclusion logic here instead of externally so alternative behaviours
    # can be set up when random.sample is out of range (exhausted number of options)
    chosen_values = random.sample(options, num_values)
    return chosen_values


def ordered_selection(
    options: list, num_values: int = 1, start_index=0
) -> list:
    logger.debug(f"Getting ordered selection from ({len(options)}) options.")
    logger.debug(f"{start_index=}")
    chosen_values = options[start_index : num_values + start_index]
    logger.debug(f"{chosen_values=}")
    return chosen_values


class ValuePickerStrategy(Enum):
    ORDERED = "ordered"  # Get the first X found files
    RANDOM = "random"  # Randomly pick from all vailable files


# Handles all internal logic for generating values to be used in project inputs.
# Is cstock job/input agnostic.
# TODO move this and file/data_picker_strategies to another file.
class CstockValuePicker:
    def __init__(
        self,
        available_values: list,
        value_picker_strategy: ValuePickerStrategy = ValuePickerStrategy.RANDOM,
        index_offset: int = 0,
        disable_state: bool = False,
    ):
        """
        A stateful value picker that remembers past choices.
        available_values: The pool of options from which to choose from.
        excluded_values: A list of options that can NOT be picked.
        disable_state: If true, past selections will not be tracked:
            For random selection: Allows the same value to be chosen more than once.
            For ordered selection: Provides a deterministic behaviour in which the same X files will be chosen.
        """
        # self.cstock_project = cstock_project
        self.available_values = available_values
        self.value_picker_strategy = value_picker_strategy
        # TODO on_values_exhausted strategy (reset state, repeat last, error, etc)

        # State config
        self._disable_state = disable_state
        # Caching/memory mechanism
        # A 'memory' for values that have already been chosen, or which are excluded from selection.
        self._previously_picked_values: list = []
        # A 'cursor' to move through an ordered selection.
        self._index_offset: int = index_offset
        logger.debug(f"Value picker instantiated:")
        logger.debug(f"\t{self.available_values=}")
        logger.debug(f"\t{self._disable_state=}")
        logger.debug(f"\t{self._previously_picked_values=}")
        logger.debug(f"\t{self._index_offset=}")

    def _get_valid_values(self):
        logger.debug(f"{self.available_values=}")
        logger.debug(f"{self._previously_picked_values=}")
        valid_values = [
            value
            for value in self.available_values
            if value not in self._previously_picked_values
        ]
        return valid_values

    def get_values(self, num_values=1) -> list:
        """
        Return a list of chosen values.
        """
        logger.debug(f"Getting values {num_values=}")
        valid_values = self._get_valid_values()
        logger.debug(f"{len(valid_values)=}")
        if self.value_picker_strategy == ValuePickerStrategy.RANDOM:
            chosen_values = random_selection(
                valid_values, num_values=num_values
            )
            logger.debug(f"\t{chosen_values=}")
            if not self._disable_state:
                self._previously_picked_values += chosen_values
                logger.debug(f"Updated {self._previously_picked_values=}")
            return chosen_values

        if self.value_picker_strategy == ValuePickerStrategy.ORDERED:
            chosen_values = ordered_selection(
                valid_values,
                num_values=num_values,
                start_index=self._index_offset,
            )
            logger.debug(f"\t{chosen_values=}")
            if not self._disable_state:
                self._index_offset += len(chosen_values)
                logger.debug(f"Updated {self._index_offset=}")
            return chosen_values
        raise Exception(
            f"Invalid value_picker_strategy {self.value_picker_strategy}: Did not return."
        )
