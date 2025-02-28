"""Data export integration to Google's BigQuery datastore.
"""
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Dict, List, Sequence, Optional
from gitlab_data_export.util import Checkpoint

import google.api_core.exceptions as goog_exc
from google.cloud import bigquery
from google.oauth2 import service_account


from .datastore import Datastore
from ..util import format_time, Result

"""
Schemas defined here are the source of truth now. If any changes are made to the schemas here, the script
will update the schema of the tables in BigQuery to match what is defined here.
"""

NOTES_SCHEMA = bigquery.SchemaField('notes', 'RECORD', mode='REPEATED', fields=[
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("body", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("attachment", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("author", "RECORD", fields=[
            bigquery.SchemaField("id", "INTEGER"),
            bigquery.SchemaField("username", "STRING"),
            bigquery.SchemaField("email", "STRING"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("state", "STRING"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
        ]),
        bigquery.SchemaField("created_at", "TIMESTAMP"),
        bigquery.SchemaField("updated_at", "TIMESTAMP"),
        bigquery.SchemaField("system", "BOOLEAN"),
        bigquery.SchemaField("noteable_id", "INTEGER"),
        bigquery.SchemaField("noteable_type", "STRING"),
        bigquery.SchemaField("project_id", "INTEGER"),
        bigquery.SchemaField("noteable_iid", "INTEGER"),
        bigquery.SchemaField("resolvable", "BOOLEAN"),
        bigquery.SchemaField("confidential", "BOOLEAN"),
        bigquery.SchemaField("internal", "BOOLEAN"),
        bigquery.SchemaField("imported", "BOOLEAN"),
        bigquery.SchemaField("imported_from", "STRING"),
    ])

EPIC_SCHEMA = [
    bigquery.SchemaField('data_date', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('iid', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('group_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('group_id', 'INTEGER'),
    bigquery.SchemaField('parent_id', 'INTEGER'),
    bigquery.SchemaField('parent_iid', 'INTEGER'),
    bigquery.SchemaField('title', 'STRING'),
    bigquery.SchemaField('description', 'STRING'),
    bigquery.SchemaField('state', 'STRING'),
    bigquery.SchemaField('confidential', 'BOOLEAN'),
    bigquery.SchemaField('web_url', 'STRING'),
    bigquery.SchemaField('reference', 'STRING'),
    bigquery.SchemaField('references', 'RECORD', fields=[
        bigquery.SchemaField('short', 'STRING'),
        bigquery.SchemaField('relative', 'STRING'),
        bigquery.SchemaField('full', 'STRING')
    ]),
    bigquery.SchemaField('author', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING')
    ]),
    bigquery.SchemaField('start_date', 'DATE'),
    bigquery.SchemaField('start_date_is_fixed', 'BOOLEAN'),
    bigquery.SchemaField('start_date_fixed', 'DATE'),
    bigquery.SchemaField('start_date_from_milestones', 'DATE'),
    bigquery.SchemaField('start_date_from_inherited_source', 'DATE'),
    bigquery.SchemaField('end_date', 'DATE'),
    bigquery.SchemaField('due_date', 'DATE'),
    bigquery.SchemaField('due_date_is_fixed', 'BOOLEAN'),
    bigquery.SchemaField('due_date_fixed', 'DATE'),
    bigquery.SchemaField('due_date_from_milestones', 'DATE'),
    bigquery.SchemaField('due_date_from_inherited_source', 'DATE'),
    bigquery.SchemaField('created_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('updated_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField("closed_at", "TIMESTAMP"),
    bigquery.SchemaField('labels', 'STRING', mode='REPEATED'),
    bigquery.SchemaField('upvotes', 'INTEGER'),
    bigquery.SchemaField('downvotes', 'INTEGER'),
    bigquery.SchemaField('color', 'STRING'),
    bigquery.SchemaField('_links', 'RECORD', fields=[
        bigquery.SchemaField('self', 'STRING'),
        bigquery.SchemaField('epic_issues', 'STRING'),
        bigquery.SchemaField('group', 'STRING'),
        bigquery.SchemaField('parent', 'STRING')
    ]),
    NOTES_SCHEMA
]

MILESTONE_SCHEMA = [
    bigquery.SchemaField('data_date', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('iid', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('location', 'STRING', mode='REQUIRED',
                         description='Where the Milestone is stored (project or group)'),
    bigquery.SchemaField('location_id', 'INTEGER', mode='REQUIRED',
                         description='The id of the Milestone\'s storage location (project or group id)'),
    bigquery.SchemaField('location_name', 'STRING', mode='REQUIRED',
                         description='The string id of the Milestone\'s storage location (project or group name)'),
    bigquery.SchemaField('title', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('description', 'STRING'),
    bigquery.SchemaField('due_date', 'DATE'),
    bigquery.SchemaField('start_date', 'DATE'),
    bigquery.SchemaField('state', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('updated_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('created_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('expired', 'BOOLEAN'),
    bigquery.SchemaField('web_url', 'STRING')
]

MERGE_REQUEST_SCHEMA = [
    bigquery.SchemaField('data_date', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('iid', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('project_id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('project_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('title', 'STRING'),
    bigquery.SchemaField('description', 'STRING'),
    bigquery.SchemaField('state', 'STRING'),
    bigquery.SchemaField('merge_user', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('merged_at', 'TIMESTAMP'),
    bigquery.SchemaField('closed_by', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('closed_at', 'TIMESTAMP'),
    bigquery.SchemaField('created_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('updated_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('target_branch', 'STRING'),
    bigquery.SchemaField('source_branch', 'STRING'),
    bigquery.SchemaField('upvotes', 'INTEGER'),
    bigquery.SchemaField('downvotes', 'INTEGER'),
    bigquery.SchemaField('author', 'RECORD', mode='REQUIRED', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('assignee', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('assignees', 'RECORD', mode='REPEATED', fields=[
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('reviewers', 'RECORD', mode='REPEATED', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('source_project_id', 'INTEGER'),
    bigquery.SchemaField('target_project_id', 'INTEGER'),
    bigquery.SchemaField('labels', 'STRING', mode='REPEATED'),
    bigquery.SchemaField('draft', 'BOOLEAN'),
    bigquery.SchemaField('work_in_progress', 'BOOLEAN'),
    bigquery.SchemaField('milestone', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('iid', 'INTEGER'),
        bigquery.SchemaField('project_id', 'INTEGER'),
        bigquery.SchemaField('title', 'STRING'),
        bigquery.SchemaField('description', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('created_at', 'TIMESTAMP'),
        bigquery.SchemaField('updated_at', 'TIMESTAMP'),
        bigquery.SchemaField('due_date', 'DATE'),
        bigquery.SchemaField('start_date', 'DATE'),
        bigquery.SchemaField('web_url', 'STRING'),
    ]),
    bigquery.SchemaField('merge_when_pipeline_succeeds', 'BOOLEAN'),
    bigquery.SchemaField('merge_status', 'STRING'),
    bigquery.SchemaField('detailed_merge_status', 'STRING'),
    bigquery.SchemaField('sha', 'STRING'),
    bigquery.SchemaField('merge_commit_sha', 'STRING'),
    bigquery.SchemaField('squash_commit_sha', 'STRING'),
    bigquery.SchemaField('user_notes_count', 'INTEGER'),
    bigquery.SchemaField('discussion_locked', 'BOOLEAN'),
    bigquery.SchemaField('should_remove_source_branch', 'BOOLEAN'),
    bigquery.SchemaField('force_remove_source_branch', 'BOOLEAN'),
    bigquery.SchemaField('allow_collaboration', 'BOOLEAN'),
    bigquery.SchemaField('allow_maintainer_to_push', 'BOOLEAN'),
    bigquery.SchemaField('web_url', 'STRING'),
    bigquery.SchemaField('references', 'RECORD', fields=[
        bigquery.SchemaField('short', 'STRING'),
        bigquery.SchemaField('relative', 'STRING'),
        bigquery.SchemaField('full', 'STRING'),
    ]),
    bigquery.SchemaField('time_stats', 'RECORD', fields=[
        bigquery.SchemaField('time_estimate', 'INTEGER'),
        bigquery.SchemaField('total_time_spent', 'INTEGER'),
        bigquery.SchemaField('human_time_estimate', 'STRING'),
        bigquery.SchemaField('human_total_time_spent',
                             'STRING'),
    ]),
    bigquery.SchemaField('squash', 'BOOLEAN'),
    bigquery.SchemaField('task_completion_status', 'RECORD', fields=[
        bigquery.SchemaField('count', 'INTEGER'),
        bigquery.SchemaField('completed_count', 'INTEGER'),
    ]),
    NOTES_SCHEMA
]

ISSUE_SCHEMA = [
    bigquery.SchemaField('data_date', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('iid', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('state', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('type', 'STRING'),
    bigquery.SchemaField('title', 'STRING'),
    bigquery.SchemaField('description', 'STRING'),
    bigquery.SchemaField('author', 'RECORD', mode='REQUIRED', fields=[
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('web_url', 'STRING'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
    ]),
    bigquery.SchemaField('milestone', 'RECORD', fields=[
        bigquery.SchemaField('project_id', 'INTEGER'),
        bigquery.SchemaField('description', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('due_date', 'DATE'),
        bigquery.SchemaField('iid', 'INTEGER'),
        bigquery.SchemaField('created_at', 'TIMESTAMP'),
        bigquery.SchemaField('title', 'STRING'),
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('updated_at', 'TIMESTAMP'),
    ]),
    bigquery.SchemaField('project_id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('project_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('assignees', 'RECORD', fields=[
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
    ], mode='REPEATED'),
    bigquery.SchemaField('assignee', 'RECORD', fields=[
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
    ]),
    bigquery.SchemaField('updated_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('closed_at', 'TIMESTAMP'),
    bigquery.SchemaField('closed_by', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('web_url', 'STRING'),
        bigquery.SchemaField('username', 'STRING'),
        bigquery.SchemaField('avatar_url', 'STRING')
    ]),
    bigquery.SchemaField('created_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('moved_to_id', 'INTEGER'),
    bigquery.SchemaField('labels', 'STRING', mode='REPEATED'),
    bigquery.SchemaField('upvotes', 'INTEGER'),
    bigquery.SchemaField('downvotes', 'INTEGER'),
    bigquery.SchemaField('merge_requests_count', 'INTEGER'),
    bigquery.SchemaField('user_notes_count', 'INTEGER'),
    bigquery.SchemaField('due_date', 'DATE'),
    bigquery.SchemaField('web_url', 'STRING'),
    bigquery.SchemaField('weight', 'INTEGER'),
    bigquery.SchemaField('epic', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('iid', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('title', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('url', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('group_id', 'INTEGER', mode='REQUIRED')
    ]),
    bigquery.SchemaField('iteration', 'RECORD', fields=[
        bigquery.SchemaField('id', 'INTEGER'),
        bigquery.SchemaField('iid', 'INTEGER'),
        bigquery.SchemaField('sequence', 'INTEGER'),
        bigquery.SchemaField('group_id', 'INTEGER'),
        bigquery.SchemaField('title', 'STRING'),
        bigquery.SchemaField('description', 'STRING'),
        bigquery.SchemaField('state', 'INTEGER'),
        bigquery.SchemaField('created_at', 'TIMESTAMP'),
        bigquery.SchemaField('updated_at', 'TIMESTAMP'),
        bigquery.SchemaField('start_date', 'DATE'),
        bigquery.SchemaField('due_date', 'DATE'),
        bigquery.SchemaField('web_url', 'STRING')
    ]),
    bigquery.SchemaField('references', 'RECORD', fields=[
        bigquery.SchemaField('short', 'STRING'),
        bigquery.SchemaField('relative', 'STRING'),
        bigquery.SchemaField('full', 'STRING')
    ]),
    bigquery.SchemaField('time_stats', 'RECORD', fields=[
        bigquery.SchemaField('time_estimate', 'INTEGER'),
        bigquery.SchemaField('total_time_spent', 'INTEGER'),
        bigquery.SchemaField('human_time_estimate', 'STRING'),
        bigquery.SchemaField('human_total_time_spent', 'STRING')
    ]),
    bigquery.SchemaField('has_tasks', 'BOOLEAN'),
    bigquery.SchemaField('task_status', 'STRING'),
    bigquery.SchemaField('confidential', 'BOOLEAN'),
    bigquery.SchemaField('discussion_locked', 'BOOLEAN'),
    bigquery.SchemaField('issue_type', 'STRING'),
    bigquery.SchemaField('severity', 'STRING'),
    bigquery.SchemaField('_links', 'RECORD', fields=[
        bigquery.SchemaField('self', 'STRING'),
        bigquery.SchemaField('notes', 'STRING'),
        bigquery.SchemaField('award_emoji', 'STRING'),
        bigquery.SchemaField('project', 'STRING'),
        bigquery.SchemaField('closed_as_duplicate_of', 'STRING')
    ]),
    bigquery.SchemaField('task_completion_status', 'RECORD', fields=[
        bigquery.SchemaField('count', 'INTEGER'),
        bigquery.SchemaField('completed_count', 'INTEGER')
    ]),
    NOTES_SCHEMA
]

CHECKPOINT_SCHEMA = [
    bigquery.SchemaField('updated_at', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('job_id', 'STRING', mode='REQUIRED')
]

LATEST_CHECKPOINT_UPSERT = R"""CREATE OR REPLACE TABLE FUNCTION `{dataset}.latest_checkpoint`(for_job_id STRING) AS (
SELECT for_job_id as job_id, MAX(c.updated_at) AS timestamp
FROM `{dataset}.Checkpoints` c
WHERE TIMESTAMP_TRUNC(updated_at, DAY) > TIMESTAMP_TRUNC(TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 4 DAY), DAY)
AND for_job_id = c.job_id
);"""

@dataclass
class Tables:
    """The tables required for BigQuery data storage."""
    epics: bigquery.Table
    milestones: bigquery.Table
    issues: bigquery.Table
    merge_requests: bigquery.Table
    checkpoints: bigquery.Table


def create_table(table_id: str, schema: List[bigquery.SchemaField]) -> bigquery.Table:
    """Creates a table description instrumented for GitLab data export.

    Note that this does not actually ensure that the table exists remotely; it is an
    in-memory representation of the table only. The BigQuery API must be used to ensure
    that the table exists in GCP.

    Args:
        table_id: the fully-qualified name of the table to create
        schema: the schema of the table to create

    Returns:
        bigquery.Table: the in-memory description of the table
    """
    table = bigquery.Table(table_id, schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY, field='updated_at')
    return table


def check_errors(errors: Sequence[Dict[str, Any]]) -> Result:
    """Checks BigQuery errors, logging and returning a Result corresponding
    to the operation's success or failure status.

    Args:
        errors: errors as returned by the BigQuery insert API
        log_extra: a dictionary of base values to log

    Returns:
        Result: the result of the operation
    """
    if errors:
        formatted = ''.join(
            [f'Error{idx}="{error}"' for idx, error in enumerate(errors)])
        logging.error(
            'Encountered one or more errors while inserting data; Errors=%s' % formatted)
        return Result.failure()
    return Result.success()


class BigQuery(Datastore):
    """Semantic access to Google's BigQuery API.

    This class is not meant to be a general-purpose API; it supports only the semantic operations
    required for data export functionality.
    """
    GOOGLE_CREDS_ENV_VAR = 'GOOGLE_APPLICATION_CREDENTIALS'
    EXPLICIT_CREDS_ENV_VAR = 'BIGQUERY_SERVICE_ACCOUNT_JSON'
    GCP_PROJECT_ENV_VAR = 'BIGQUERY_PROJECT'
    BQ_DATASET_ENV_VAR = 'BIGQUERY_DATASET'

    def __init__(self, gitlab_api_version='v4'):
        logging.debug('Initializing BigQuery datastore backend')
        self.client = self.client_from_env()
        self.project = os.getenv(self.GCP_PROJECT_ENV_VAR, None)
        if self.project is None:
            raise ValueError(
                f'GCP project unset; {self.GCP_PROJECT_ENV_VAR} must be provided')
        self.dataset = os.getenv(
            self.BQ_DATASET_ENV_VAR, 'gitlab_data_export') + '_' + gitlab_api_version
        logging.info("Target Dataset: {}".format(self.dataset))
        self.tables = Tables(
            epics=create_table(f'{self.fq_dataset}.Epics', EPIC_SCHEMA),
            milestones=create_table(
                f'{self.fq_dataset}.Milestones', MILESTONE_SCHEMA),
            issues=create_table(
                f'{self.fq_dataset}.Issues', ISSUE_SCHEMA),
            merge_requests=create_table(
                f'{self.fq_dataset}.MergeRequests', MERGE_REQUEST_SCHEMA),
            checkpoints=create_table(
                f'{self.fq_dataset}.Checkpoints', CHECKPOINT_SCHEMA)
        )
        logging.debug(
            'BigQuery datastore backend initialized successfully; Dataset=%s' % self.fq_dataset)

    @classmethod
    def client_from_env(cls) -> bigquery.Client:
        """Constructs a BigQuery client from the currently available environment variables.

        Raises:
            ValueError: if no authentication method could be found

        Returns:
            bigquery.Client
        """
        if cls.GOOGLE_CREDS_ENV_VAR in os.environ:
            logging.debug(
                'Initializing BigQuery using Google application credentials')
            return bigquery.Client()
        explicit_creds = os.getenv(cls.EXPLICIT_CREDS_ENV_VAR, None)
        if explicit_creds is not None:
            logging.debug('Initializing BigQuery using service account JSON')
            creds = service_account.Credentials.from_service_account_info(
                json.loads(explicit_creds))
            return bigquery.Client(credentials=creds)

        raise ValueError(
            f'Could not authenticate to BigQuery; one of {cls.GOOGLE_CREDS_ENV_VAR} or {cls.EXPLICIT_CREDS_ENV_VAR} must be provided')

    @property
    def fq_dataset(self):
        """Returns the fully-qualified dataset name used by the instance.
        """
        return f'{self.project}.{self.dataset}'

    def ensure_dataset_exists(self):
        """Ensures that the data export dataset exists.
        """
        logging.info('Ensuring dataset exists; Dataset=%s' % self.fq_dataset)
        self.client.create_dataset(self.fq_dataset, exists_ok=True)

    def _ensure_table(self, table: bigquery.Table):
        logging.info('Ensuring table exists; Table=%s' % table.table_id)
        self.client.create_table(table, exists_ok=True)

    def _ensure_table_function(self, upsert_query: str):
        return self.client.query(upsert_query).result()

    def ensure_tables_exist(self):
        """Ensures that all required tables exist.
        """
        self._ensure_table(self.tables.epics)
        self._ensure_table(self.tables.milestones)
        self._ensure_table(self.tables.issues)
        self._ensure_table(self.tables.merge_requests)
        self._ensure_table(self.tables.checkpoints)
    
    
    def _schema_diff(self, table: bigquery.Table, bq_table: bigquery.Table):
        """Checks if there are any fields in the table schema defined in code that are not present in the BigQuery table schema.
        Will only ADD columns to BigQuery table Schema. Will not remove any.

        Args:
            table (bigquery.Table): Internal Table definition
            bq_table (bigquery.Table): Table object from BigQuery API
        """
        new_fields = [field for field in table.schema if field not in bq_table.schema]
        if new_fields:
            logging.info('Schema difference detected between tables. Updating BigQuery table schema to match pipeline table schema; Table={}'.format(bq_table.table_id))
            new_schema = bq_table.schema
            for field in new_fields:
                new_schema.append(field)
            bq_table.schema = new_schema
            self.client.update_table(bq_table, ['schema'])

    def ensure_table_schemas(self):
        """Ensures table schemas in BigQuery all match what is defined here in code.
        """
        logging.info('Ensuring schemas defined in pipeline match schemas of tables in BigQuery.')
        self._schema_diff(self.tables.epics, self.client.get_table(table=self.tables.epics))
        self._schema_diff(self.tables.milestones, self.client.get_table(table=self.tables.milestones))
        self._schema_diff(self.tables.issues, self.client.get_table(table=self.tables.issues))
        self._schema_diff(self.tables.merge_requests, self.client.get_table(table=self.tables.merge_requests))
        self._schema_diff(self.tables.checkpoints, self.client.get_table(table=self.tables.checkpoints))

    def ensure_table_functions_exist(self):
        """Ensures that all required table functions exist.
        """
        self._ensure_table_function(LATEST_CHECKPOINT_UPSERT.format(dataset=self.fq_dataset))

    def ensure_storage(self):
        self.ensure_dataset_exists()
        self.ensure_tables_exist()
        self.ensure_table_schemas()
        self.ensure_table_functions_exist()

    def _durable_insert(self, table: bigquery.Table, rows: Iterable[Dict[str, Any]]) -> Sequence[Dict[str, Any]]:
        attempts = 0
        while attempts < 3:
            try:
                return self.client.insert_rows(
                    table, rows, ignore_unknown_values=True)
            except goog_exc.NotFound:
                attempts += 1
        return self.client.insert_rows(table, rows, ignore_unknown_values=True)

    def insert_epics(self, data_date: datetime, group_name: str, epics: Iterable[Dict[str, Any]]) -> Result:
        logging.info('Inserting Epics; Dataset=%s' % self.fq_dataset)
        for epic in epics:
            epic['data_date'] = format_time(data_date)
            epic['group_name'] = group_name

        return check_errors(self._durable_insert(self.tables.epics, epics))

    def insert_milestones(self, data_date: datetime, location_name: str, milestones: Iterable[Dict[str, Any]]) -> Result:
        logging.info('Inserting Milestones; Dataset=%s' % self.fq_dataset)
        for milestone in milestones:
            milestone['data_date'] = format_time(data_date)
            milestone['location_name'] = location_name
            if 'project_id' in milestone:
                milestone['location'] = 'project'
                milestone['location_id'] = milestone.pop('project_id')
            elif 'group_id' in milestone:
                milestone['location'] = 'group'
                milestone['location_id'] = milestone.pop('group_id')

        return check_errors(self._durable_insert(self.tables.milestones, milestones))

    def insert_issues(self, data_date: datetime, project_name: str, issues: Iterable[Dict[str, Any]]) -> Result:
        logging.info('Inserting Issues; Dataset=%s' % self.fq_dataset)
        for issue in issues:
            issue['data_date'] = format_time(data_date)
            issue['project_name'] = project_name

        return check_errors(self._durable_insert(self.tables.issues, issues))

    def insert_merge_requests(self, data_date: datetime, project_name: str, merge_requests: Iterable[Dict[str, Any]]) -> Result:
        logging.info('Inserting Merge Requests; Dataset=%s' % self.fq_dataset)
        for mr in merge_requests:
            mr['data_date'] = format_time(data_date)
            mr['project_name'] = project_name

        return check_errors(self._durable_insert(self.tables.merge_requests, merge_requests))
    
    def load_previous_checkpoint(self, checkpoint_job_id) -> Optional[Checkpoint]:
        logging.info(f'Attempting to load checkpoint from BigQuery; Dataset={self.fq_dataset}, JobId={checkpoint_job_id}')
        job_config = bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter('job_id', 'STRING', checkpoint_job_id)
        ])
        job = self.client.query(f'select job_id, timestamp from `{self.fq_dataset}.latest_checkpoint`(@job_id)',
                                job_config=job_config)
        for row in job.result():
            if row['timestamp'] is not None:
                return Checkpoint(job_id=row['job_id'], timestamp=row['timestamp'])
        logging.info(f'Could not find previous checkpoint for job_id={checkpoint_job_id}, defaulting to historical backfill.')
        return None

    def persist_checkpoint(self, checkpoint: Checkpoint) -> Result:
        logging.info('Persisting checkpoint; Dataset=%s' % self.fq_dataset)
        cp = {'updated_at': format_time(checkpoint.timestamp), 'job_id': checkpoint.job_id}
        return check_errors(self._durable_insert(self.tables.checkpoints, [cp]))

        