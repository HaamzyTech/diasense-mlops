# Test Report Template

## Metadata
- Date:
- Environment (local/CI):
- Git commit hash:
- DVC revision:
- MLflow run ID:
- Tester:

## Scope
- Components tested:
- Out-of-scope:

## Results Summary
- Total tests:
- Passed:
- Failed:
- Blocked:

## Execution Log
| Test ID | Category | Command/Procedure | Expected | Actual | Status |
|---|---|---|---|---|---|
| UT-001 | Unit | `pytest -q ml/tests` | pass |  |  |
| IT-001 | Integration | `pytest -q apps/backend-api/tests` | pass |  |  |
| API-001 | API | `curl http://localhost:8000/api/v1/health` | 200 + status ok |  |  |
| PIPE-001 | Pipeline | `dvc repro` | all stages complete |  |  |

## Defects
| Defect ID | Severity | Component | Description | Repro Steps | Status |
|---|---|---|---|---|---|

## Sign-off
- QA reviewer:
- Engineering reviewer:
- Decision (Go/No-Go):
