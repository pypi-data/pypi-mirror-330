# GitLab Data Export

`gitlab-data-export` is a simple utility that exports data from GitLab's REST API into arbitrary data stores.

## Basics

`gitlab-data-export` is designed to be run from directly within GitLab itself using [scheduled CI
pipelines](https://docs.gitlab.com/ee/ci/pipelines/schedules.html).
Each time the tool is invoked, it searches for a checkpoint persisted from a previous invocation to determine
the subset of data that should be exported from the API; if no checkpoint can be found, a historical backfill
is run over _all_ GitLab resources to seed the data store.  This checkpoint is stored within the datastore
keyed off the variable CHECKPOINT_JOB_ID.

Generally, all data that GitLab provides from its API should be available in the exported data.

Data can be exported from GitLab groups or projects. By default, exporting data from a group will also recursively
export all data visible from that group's contained projects and all of its subgroups. This may comprise a large
amount of data; recursive behavior can be disabled by using [optional configurations](#optional).

## Quickstart

By default, `gitlab-data-export` will export data to [BigQuery](#bigquery). This requires a properly configured
GCP project as described in [Google's offical documentation](https://cloud.google.com/bigquery/docs). Once the project
is configured, exporting data is straightforward:

1. Create a [GitLab access token](https://docs.gitlab.com/ee/security/token_overview.html) with `read_api` permissions
   to the resources that you wish to export
2. Create a [service account keyfile](https://cloud.google.com/bigquery/docs/use-service-accounts) with `BigQuery Data
   Editor` permissions in your BigQuery-enabled GCP project
3. Create a GitLab project to run the CI pipeline
    * You can also use an existing project - only a single CI job definition is required
4. Set the [required environment variables](#required) in the GitLab project's CI/CD settings
    * The [BigQuery backend](#bigquery) also has required configurations that must be set
5. Add the following stanza to the GitLab project's [CI
   configuration](https://docs.gitlab.com/ee/ci/yaml/gitlab_ci_yaml.html):

```yaml
gitlab_export:
  image: python:3.11
  interruptible: true
  needs: []
  variables:
    CHECKPOINT_JOB_ID: $CI_JOB_NAME
  before_script:
    - python3.11 -m pip install gitlab_data_export --upgrade
  script:
    - python3.11 -m gitlab_data_export.driver
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      allow_failure: true
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

6. Optionally, [run the pipeline
   manually](https://docs.gitlab.com/ee/ci/pipelines/#add-manual-interaction-to-your-pipeline) to ensure that everything
   is working properly
    * **Important**: the first export invocation will export **ALL** history visible from the GitLab resource
    that you've configured. **This could potentially comprise a large amount of data that will incur BigQuery costs**.
    If you do not want a historical backfill to be performed, see the [optional configuration](#optional) for details
    on how to disable this behavior
7. Merge the CI changes

The pipeline should now run according to your chosen frequency and incrementally export data each time the utility
is invoked. Some query examples specific to the BigQuery storage backend can be found in the
[BigQuery section below](#bigquery).

## Configuration

`gitlab-data-export` supports a number of configuration options. All configuration is managed via environment variables.

### Required

* GitLab authentication: either `GITLAB_TOKEN` or `GITLAB_OAUTH` must be set
    * `GITLAB_TOKEN`, if set, should contain a GitLab access token
    * `GITLAB_OAUTH`, if set, should contain GitLab OAuth credentials
    * If both are set, `GITLAB_TOKEN` will take precedence
* GitLab root resource: either `GITLAB_GROUP` or `GITLAB_PROJECT` must be set
    * `GITLAB_GROUP`, if set, should contain a fully-qualified path to a GitLab group
    * `GITLAB_PROJECT`, if set, should contain a fully-qualified path to a GitLab project
* Checkpoint job id: `CHECKPOINT_JOB_ID` must be set
    * This should be unique per GitLab job section
    * Is used as the identifier for storing where a job last left off

### Optional

* `GITLAB_URL`: override the GitLab instance from which data should be exported
    * Defaults to `https://gitlab.com` if unset
* `GITLAB_BACKFILL_TIMESTAMP`: if set, overrides the default historical backfill behavior by limiting the
  `updated_after` time of GitLab resources. Accepted values are either `now` or a timestamp in `%Y-%m-%d %H:%M:%S`
  format. `now` disables backfill completely, while a timestamp limits backfill
* `GITLAB_NO_RECURSION`: if set (to any value), completely disables group recursion

## Data storage design

Data is treated as append-only. Once written, records are _never_ modified or deleted. In addition to the data
retrieved from the API, every record is enriched with a `data_date` field that users can rely upon in analytical
queries, representing the time at which the records were loaded into BigQuery.

The "latest" state for each resource can always be found by grouping by `id` and selecting the greatest
`updated_at`. Because all written records contain all information returned by the API, this design provides easy
access to the latest state of each record while also providing a basic form of historical "snapshots".

For more granular history, users need only run `gitlab-data-export` more frequently. Naturally, more granular
history also implies a greater level of data duplication - choose your export frequency accordingly. For most
use-cases, daily export should be sufficient.

## Supported data stores

Each supported data store may carry its own bespoke requirements and configurations. These details are described
for each implemented store.

### BigQuery

The BigQuery backend requires the following configurations:

* Authentication: either `GOOGLE_APPLICATION_CREDENTIALS` or `BIGQUERY_SERVICE_ACCOUNT_JSON` must be set
    * `GOOGLE_APPLICATION_CREDENTIALS`, if set, should contain [Google default
      credentials](https://cloud.google.com/bigquery/docs/authentication/getting-started)
    * `BIGQUERY_SERVICE_ACCOUNT_JSON`, if set, should contain [a Google service account
      key](https://cloud.google.com/bigquery/docs/authentication/service-account-file)
* `BIGQUERY_PROJECT`: the globally unique project id for the BigQuery-enabled GCP project to use for data storage

The following optional configurations are also supported:

* `BIGQUERY_DATASET`: can be set to override the dataset name that will be populated with GitLab data
    * Defaults to `gitlab_data_export` if unset
    * Note that the dataset name will **always** have the GitLab API version appended to it for future
    compatibility purposes