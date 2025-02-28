"""Ubiquitously useful utilities."""
from __future__ import annotations
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


def format_time(dt: datetime) -> str:
    """Formats a datetime to ISO standard format."""
    return dt.strftime(TIMESTAMP_FORMAT)


def parse_time(dt: str) -> datetime:
    """Parses a datetime from an ISO standard format string."""
    return datetime.strptime(dt, TIMESTAMP_FORMAT)


class Result:
    """Models the possibility of generic and composable failure of multiple operations.
    """

    def __init__(self, successful: bool):
        self.successful = successful

    def bind(self, other: Result):
        """Monadically consumes another result, binding the final result.

        Any failure along an operation's chain is defined as a failure of the entire operation.

        Args:
            other: the Result to bind
        """
        if self.successful:
            self.successful = other.successful

    def ensure(self):
        """Ensures that the operation was successful, aborting the program if it was not.
        """
        if not self.successful:
            logging.error('One or more errors detected; aborting')
            sys.exit(255)

    @staticmethod
    def success() -> Result:
        """Creates a successful Result."""
        return Result(successful=True)

    @staticmethod
    def failure() -> Result:
        """Creates a failed Result."""
        return Result(successful=False)


@dataclass
class Checkpoint:
    """A persisted checkpoint and job id"""
    timestamp: datetime # in utc
    job_id: str


@dataclass
class ExportOptions:
    """Options that users can customize to influence export behavior."""
    backfill_time: str
    recursion_enabled: bool

    @property
    def backfill_disabled(self) -> bool:
        """Whether historical backfill is completely disabled."""
        return self.backfill_time.lower() == 'now'

    def backfill_timestamp(self, now: datetime) -> datetime:
        """Retrieves the timestamp that should be used for historical backfill.

        Args:
            now: the timestamp for the current data export invocation
        """
        return now if self.backfill_disabled else parse_time(self.backfill_time)

    @staticmethod
    def from_env() -> ExportOptions:
        """Constructs ExportOptions from the current environment."""
        return ExportOptions(
            os.getenv('GITLAB_BACKFILL_TIMESTAMP', '1970-01-01 00:00:00'),
            'GITLAB_NO_RECURSION' not in os.environ
        )
