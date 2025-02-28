"""Abstraction of external data storage plugin architecture."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterable, Dict, Optional

from ..util import Result, Checkpoint


class Datastore(ABC):
    """A Datastore is an integration with an external data storage mechanism.

    Data exported from the GitLab API must be stored in a durable destination for
    future analytics. Each Datastore implementation provides an option for this data
    storage.

    All methods may raise arbitrary exceptions specific to the external storage
    implementation. Users are expected to understand the details of their selected
    external store and to handle exceptions accordingly.

    There are a few requirements expected of an external store in order to make it
    Datastore compatible:

    TODO
    """

    @abstractmethod
    def ensure_storage(self):
        """Ensures that external storage exists and is properly configured for data
        ingress. After this method returns successfully, the external store should be
        ready to accept data from the GitLab API.
        """

    @abstractmethod
    def insert_epics(self, data_date: datetime, group_name: str, epics: Iterable[Dict[str, Any]]) -> Result:
        """Inserts Epics into the external store.

        If the operation fails completely (e.g., connectivity to the store could not be established),
        an exception should be raised.

        If a portion of the operation semantically fails (e.g., a single row could not be inserted
        due to a constraint violation), the implementation should log an error and return a failed
        Result; otherwise, a successful Result should be returned.

        Args:
            data_date: the timestamp for the export invocation
            group_name: the name of the group containing the epics
            epics: the Epics (in JSON format) to insert

        Returns:
            result: a Result indicating whether a portion of the insert operation failed; meant for
            semantic failures rather then operational failures
        """

    @abstractmethod
    def insert_milestones(self, data_date: datetime, location_name: str, milestones: Iterable[Dict[str, Any]]) -> Result:
        """Inserts Milestones into the external store.

        If the operation fails completely (e.g., connectivity to the store could not be established),
        an exception should be raised.

        If a portion of the operation semantically fails (e.g., a single row could not be inserted
        due to a constraint violation), the implementation should log an error and return a failed
        Result; otherwise, a successful Result should be returned.

        Args:
            data_date: the timestamp for the export invocation
            location_name: the name of the resource containing the milestones
            milestones: the Milestones (in JSON format) to insert

        Returns:
            result: a Result indicating whether a portion of the insert operation failed; meant for
            semantic failures rather then operational failures
        """

    @abstractmethod
    def insert_issues(self, data_date: datetime, project_name: str, issues: Iterable[Dict[str, Any]]) -> Result:
        """Inserts issues into the external store.

        If the operation fails completely (e.g., connectivity to the store could not be established),
        an exception should be raised.

        If a portion of the operation semantically fails (e.g., a single row could not be inserted
        due to a constraint violation), the implementation should log an error and return a failed
        Result; otherwise, a successful Result should be returned.

        Args:
            data_date: the timestamp for the export invocation
            project_name: the name of the project containing the issues
            issues: the issues (in JSON format) to insert

        Returns:
            result: a Result indicating whether a portion of the insert operation failed; meant for
            semantic failures rather then operational failures
        """

    @abstractmethod
    def insert_merge_requests(self, data_date: datetime, project_name: str, merge_requests: Iterable[Dict[str, Any]]) -> Result:
        """Inserts merge requests into the external store.

        If the operation fails completely (e.g., connectivity to the store could not be established),
        an exception should be raised.

        If a portion of the operation semantically fails (e.g., a single row could not be inserted
        due to a constraint violation), the implementation should log an error and return a failed
        Result; otherwise, a successful Result should be returned.

        Args:
            data_date: the timestamp for the export invocation
            project_name: the name of the project containing the merge requests
            merge_requests: the merge requests (in JSON format) to insert

        Returns:
            result: a Result indicating whether a portion of the insert operation failed; meant for
            semantic failures rather then operational failures
        """

    @abstractmethod
    def load_previous_checkpoint(self, checkpoint_job_id) -> Optional[Checkpoint]:
        """Loads the previously persisted checkpoint timestamp in utc for the given job.

        Args:
            checkpoint_job_id: the unique identifier of the export job to load the checkpoint for

        Returns:
            Optional[Checkpoint]: the previously persisted checkpoint or None if no such
            checkpoint could be found
        """

    @abstractmethod
    def persist_checkpoint(self, checkpoint: Checkpoint) -> Result:
        """Persists the current checkpoint timestamp in utc for the given job.

        Args:
            checkpoint: the checkpoint to persist

        Returns:
            result: a Result indicating whether a portion of the update checkpoint operation failed;
            meant for semantic failures rather then operational failures
        """
