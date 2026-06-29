# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Sample of app's CLI output to see what a generated plan looks like:

```
TODOOOOOOOOOO
```

## 🧪 Testing PawPal+



```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

### Test Coverage

The test suite (`tests/test_pawpal.py`) includes 13 tests covering:

1. **Task Management** — Creating tasks, marking complete, tracking status changes
2. **Pet & Owner Operations** — Adding pets, resolving pet identity for duplicate task names
3. **Scheduling Correctness** — Tasks scheduled in chronological order by start time
4. **Recurrence Logic** — Daily and weekly task recurrence creates next occurrences correctly
5. **Conflict Detection** — Detects overlapping incompatible tasks; permits parallel execution for same-breed pets doing the same task
6. **Time Management** — Tasks finish by their due times; different pet types are scheduled sequentially to avoid conflicts
7. **Mixed Recurrence** — Daily and weekly tasks coexist without conflicts

Key tests verify:
- ✓ Sorting correctness: tasks returned in chronological order
- ✓ Recurrence logic: daily task completion creates next day's task
- ✓ Conflict detection: overlapping incompatible tasks are flagged
- ✓ Parallel execution: same task for same-breed pets runs simultaneously
- ✓ Sequential scheduling: same task for different-breed pets avoids conflicts

Confidence Level: 4 stars - all tests past, not 100% if every possible edge case has been handled or super complex conflicts have been able to be resolved

Sample test output:

```
PS C:\Users\jbous\git\CodePath AI\ai110-module2show-pawpal-starter> python -m pytest                                                                                      
============================================================================== test session starts ==============================================================================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\jbous\git\CodePath AI\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 13 items                                                                                                                                                               

tests\test_pawpal.py .............                                                                                                                                         [100%]

============================================================================== 13 passed in 0.14s ===============================================================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `sort_tasks()` | Sorts daily task list by scheduled start time, with fallback to due datetime if not yet scheduled (O(n log n)) |
| Filtering | `filter_tasks(status, pet_name, owner)` | Filters tasks by completion status (pending/complete) and/or pet name; optional parameters allow single or combined filtering |
| Conflict handling | `detect_conflicts(owner, tasks)` | Detects overlapping time slots; permits same task for same-breed pets to run in parallel; flags incompatible tasks (different breeds, different task names) |
| Recurring tasks | `complete_task(task, owner)` + `Task.next_occurrence()` | Marks task complete, removes from schedule, and creates next occurrence (daily/weekly) via recurrence pattern; links new task back to pet |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
