from ddeutil.observe.routes.workflow.schemas import (
    ReleaseLogCreate,
    WorkflowCreate,
)


def test_workflow_schema():
    # NOTE: This data return from ddeutil-workflow api.
    value = {
        "name": "wf-scheduling",
        "params": {"asat-dt": {"type": "datetime"}},
        "on": [
            {"cronjob": "*/3 * * * *", "timezone": "Asia/Bangkok"},
            {"cronjob": "* * * * *", "timezone": "Asia/Bangkok"},
        ],
        "jobs": {
            "condition-job": {
                "id": "condition-job",
                "stages": [
                    {"name": "Empty stage"},
                    {
                        "name": "Call-out",
                        "echo": "Hello ${{ params.asat-dt | fmt('%Y-%m-%d') }}",
                    },
                ],
            }
        },
    }
    rs = WorkflowCreate.model_validate(value)
    assert rs.name == "wf-scheduling"


def test_workflow_schema_log():
    value = {
        "release": "20240902093600",
        "logs": [
            {
                "run_id": "635351540020240902093554579053",
                "context": {
                    "name": "wf-scheduling",
                    "on": "*/3 * * * *",
                    "release": "2024-09-02 09:36:00+07:00",
                    "context": {
                        "params": {"asat-dt": "2024-09-02 09:36:00+07:00"},
                        "jobs": {
                            "condition-job": {
                                "matrix": {},
                                "stages": {
                                    "6708019737": {"outputs": {}},
                                    "0663452000": {"outputs": {}},
                                },
                            }
                        },
                    },
                    "parent_run_id": "635351540020240902093554579053",
                    "run_id": "635351540020240902093554579053",
                    "update": "2024-09-02 09:35:54.579053",
                },
            },
        ],
    }
    rs = ReleaseLogCreate.model_validate(value)
    assert rs.release == 20240902093600
