"""Interaction with GitLab's REST API."""
import logging
import os
from datetime import datetime
from enum import Enum
from typing import (Any, Callable, Dict, Iterable,
                    Optional, List, Tuple, TypeVar, Union)

import gitlab
import gitlab.base

from ..util import format_time, parse_time, ExportOptions, Result, Checkpoint
from .datastore import Datastore


class AuthType(Enum):
    """GitLab authentication types.
    """
    GITLAB_TOKEN = 1
    GITLAB_OAUTH = 2


Auth = Tuple[AuthType, str]

ignore_bots_env = os.environ.get("IGNORE_BOTS", "")
IGNORE_BOTS = set(ignore_bots_env.split(','))  # Convert to a set

def auth_from_env() -> Auth:
    """Retrieves authentication credentials from the current environment.

    Raises:
        ValueError: if no credential can be extracted from the environment

    Returns:
        Auth: credentials to use for authentication against GitLab's REST API
    """
    token = os.environ.get(AuthType.GITLAB_TOKEN.name)
    oauth = os.environ.get(AuthType.GITLAB_OAUTH.name)
    if token is not None:
        logging.debug('Authenticating to GitLab using access token')
        return AuthType.GITLAB_TOKEN, token
    elif oauth is not None:
        logging.debug('Authenticating to GitLab using OAuth token')
        return AuthType.GITLAB_OAUTH, oauth
    else:
        raise ValueError(
            f'At least one of the environment variables "{AuthType.GITLAB_TOKEN.name}" or "{AuthType.GITLAB_OAUTH.name}" must be set')


class ResourceType(Enum):
    """GitLab resource types supporting data export."""
    GITLAB_GROUP = 1
    GITLAB_PROJECT = 2


Resource = Tuple[ResourceType, str]


def resource_from_env() -> Resource:
    """Retrieves the resource to export from the current environment.

    Group resources are preferred if multiple resources are provided.

    Raises:
        ValueError: if no resource can be extracted from the environment

    Returns:
        Resource: the resource to export from GitLab's REST API
    """
    group = os.environ.get(ResourceType.GITLAB_GROUP.name)
    project = os.environ.get(ResourceType.GITLAB_PROJECT.name)
    if group is not None:
        return ResourceType.GITLAB_GROUP, group
    elif project is not None:
        return ResourceType.GITLAB_PROJECT, project
    else:
        raise ValueError(
            f'At least one of the environment variables "{ResourceType.GITLAB_GROUP.name}" or "{ResourceType.GITLAB_PROJECT.name}" must be set')


GitlabRestResponse = Union[gitlab.base.RESTObjectList,
                           List[gitlab.base.RESTObject]]
RESOURCES_PER_PAGE = 100


def paginated(after: datetime, before: datetime,
              query: Callable[..., GitlabRestResponse]) -> Iterable[List[Dict[str, Any]]]:
    """Automatically paginates the results of a GitLab REST operation.

    Args:
        after: an earliest time bound for GitLab resource modifications
        before: a latest time bound for GitLab resource modifications
        query: the GitLab REST operation to run

    Returns:
        Iterable[List[Dict[str, Any]]]: chunks of results yielded by the GitLab API
    """
    page = 1
    while True:
        page_results = query(updated_after=format_time(after),
                             updated_before=format_time(before),
                             per_page=RESOURCES_PER_PAGE,
                             page=page)
        yield [result.asdict() for result in page_results]
        if len(page_results) < RESOURCES_PER_PAGE:
            break
        page = page + 1


def _kwargs_from_auth(auth: Auth) -> Dict[str, Any]:
    (auth_type, cred) = auth
    if auth_type == AuthType.GITLAB_TOKEN:
        return {'private_token': cred}
    elif auth_type == AuthType.GITLAB_OAUTH:
        return {'oauth_token': cred}
    raise NotImplementedError(
        f'Unimplemented authentication type: {auth_type.name}')


class Gitlab:
    """Semantic access to GitLab's REST API.

    This class is not meant to be a general-purpose API; it supports only the semantic operations
    required for data export functionality.
    """
    GITLAB_DEFAULT_URL = 'https://gitlab.com'
    GITLAB_URL_VAR = 'GITLAB_URL'

    def __init__(self, url: Optional[str] = None, auth: Optional[Auth] = None,
                 resource: Optional[Resource] = None, options: Optional[ExportOptions] = None):
        self.url = url or os.getenv(
            self.GITLAB_URL_VAR, self.GITLAB_DEFAULT_URL)
        logging.debug('Initializing GitLab API connection to %s' % self.url)
        self.auth = auth or auth_from_env()
        self.resource = resource or resource_from_env()
        self.options = options or ExportOptions.from_env()
        self.gitlab = gitlab.Gitlab(self.url, **_kwargs_from_auth(self.auth))
        self.gitlab.auth()

    def _export_project(self, project_id: str, datastore: Datastore, since: datetime,
                        until: datetime) -> Result:
        logging.info('Exporting project data; Project=%s; Since=%s; Until=%s' %
                     (project_id, format_time(since), format_time(until)))
        result = Result.success()
        project = self.gitlab.projects.get(project_id)

        records = 0
        for milestones in paginated(since, until, project.milestones.list):
            if milestones:
                records += len(milestones)
                result.bind(datastore.insert_milestones(
                    until, project_id, milestones))
        logging.info('Inserted Milestones; Count=%s' % records)

        records = 0
        for issues in paginated(since, until, project.issues.list):
            if issues:
                # fetch project notes
                self._export_notes(project.issues, issues)
                records += len(issues)
                result.bind(datastore.insert_issues(until, project_id, issues))
        logging.info('Inserted Issues; Count=%s' % records)

        records = 0
        for merge_requests in paginated(since, until, project.mergerequests.list):
            if merge_requests:
                # fetch project notes
                self._export_notes(project.mergerequests, merge_requests)
                records += len(merge_requests)
                result.bind(datastore.insert_merge_requests(
                    until, project_id, merge_requests))
        logging.info('Inserted Merge Requests; Count=%s' % records)

        return result

    def _export_group(self, group_id: str, datastore: Datastore, since: datetime,
                      until: datetime) -> Result:
        logging.info('Exporting group data; Group=%s; Since=%s; Until=%s' %
                     (group_id, format_time(since), format_time(until)))
        result = Result.success()
        group = self.gitlab.groups.get(group_id)

        records = 0
        for epics in paginated(since, until, group.epics.list):
            epics = [e for e in epics if e['group_id'] == group.attributes['id']]
            if epics:
                # fetch group notes
                self._export_notes(group.epics, epics)
                records += len(epics)
                result.bind(datastore.insert_epics(until, group_id, epics))
        logging.info('Inserted Epics; Count=%s' % records)

        records = 0
        for milestones in paginated(since, until, group.milestones.list):
            if milestones:
                records += len(milestones)
                result.bind(datastore.insert_milestones(
                    until, group_id, milestones))
        logging.info('Inserted Milestones; Count=%s' % records)

        if self.options.recursion_enabled:
            for project in group.projects.list(get_all=True):
                result.bind(self._export_project(
                    project.path_with_namespace, datastore, since, until))

            for subgroup in group.subgroups.list(get_all=True):
                result.bind(self._export_group(subgroup.full_path,
                                               datastore, since, until))
        else:
            logging.info(
                'Group recursion disabled, skipping subgroups and subprojects')

        return result

    # Milestones do not contain notes, so do not need to include those here.
    def _export_notes(self, collection_manager, items):
        """Fetches notes for each item in a given list of items and inserts them in
        item dictionary.

        Args:
            collection_manager (Gitlab Manager Object): Manager object of one of the following types:
                - gitlab.v4.objects.epics.GroupEpicManager
                - gitlab.v4.objects.issues.ProjectIssueManager
                - gitlab.v4.objects.merge_requests.ProjectMergeRequestManager
                - gitlab.v4.objects.issues.ProjectIssueManager
            items (list): List of dictionaries of paginated items.
        """
        for item in items:
            try:
                sourced_object = collection_manager.get(item['iid'])
            except gitlab.exceptions.GitlabGetError:
                logging.warning('Failed to retrieve notes for item %s', item['iid'])
                continue
            filter = lambda note: not note.asdict()['author']['username'] in IGNORE_BOTS
            item['notes'] = [note.asdict() for note in sourced_object.notes.list(iterator=True) if filter(note)]
        
    def export_data(self, datastore: Datastore, checkpoint_job_id: str,
                    now=None) -> Result:
        """Exports data to an external store based on the previous checkpoint.

        If the provided datastore provides no checkpoint, a historical backfill up to the current time
        will be performed; if the GITLAB_BACKFILL_OVERRIDE environment variable is set to True, the job will ignore the most recent checkpoint
        and a historical backfill up to the current time will be performed; otherwise, only data that has been updated since the checkpoint
        will be inserted.

        Args:
            datastore: a Datastore implementation
            checkpoint_job_id: the unique identifier of the export job to load the checkpoint for
            now: a datetime representing the current time in UTC
        """
        datastore.ensure_storage()
        now = now or datetime.utcnow()
        if os.getenv('GITLAB_BACKFILL_OVERRIDE', False):
            logging.info('Backfill override detected, running backfill since configured date.')
            since = self.options.backfill_timestamp(now)
        else:
            checkpoint = datastore.load_previous_checkpoint(checkpoint_job_id)
            since = checkpoint.timestamp if checkpoint is not None else self.options.backfill_timestamp(
                now)

        resource_type, identifier = self.resource
        result = Result.success()
        if resource_type == ResourceType.GITLAB_PROJECT:
            result.bind(self._export_project(
                identifier, datastore, since, now))
        elif resource_type == ResourceType.GITLAB_GROUP:
            result.bind(self._export_group(
                identifier, datastore, since, now))
        else:
            raise ValueError(f'Unknown resource type {resource_type}')

        result.bind(datastore.persist_checkpoint(Checkpoint(now, checkpoint_job_id)))
        return result
