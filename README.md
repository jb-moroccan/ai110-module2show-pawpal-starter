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

## 🖥️ Sample of app's CLI output to see what a generated plan looks like:

```
All tasks — Owner: Alex
------------------
08:00 — Feed (Buddy) (15 min) [priority: 1] [complete]
09:00 — Feed (Mittens) (10 min) [priority: 1] [pending]
10:00 — Fetch (Buddy) (20 min) [priority: 2] [pending]
10:00 — Fetch (Max) (20 min) [priority: 2] [pending]
11:00 — Groom (Buddy) (30 min) [priority: 1] [pending]
11:00 — Groom (Mittens) (30 min) [priority: 1] [pending]
12:30 — Walk (Buddy) (30 min) [priority: 3] [pending]

Pending tasks:
09:00 — Feed (Mittens) (10 min) [priority: 1] [pending]
10:00 — Fetch (Buddy) (20 min) [priority: 2] [pending]
10:00 — Fetch (Max) (20 min) [priority: 2] [pending]
11:00 — Groom (Buddy) (30 min) [priority: 1] [pending]
11:00 — Groom (Mittens) (30 min) [priority: 1] [pending]
12:30 — Walk (Buddy) (30 min) [priority: 3] [pending]

Completed tasks:
08:00 — Feed (Buddy) (15 min) [priority: 1] [complete]

Today's schedule from owner Alex (with scheduled times):
Owner must start at: 08:50
--------------------------------------------------------------------------------
[08:50-09:00] Feed                 (Mittens   ) due 09:00 (10 min) [priority: 1]
[09:40-10:00] Fetch                (Buddy     ) due 10:00 (20 min) [priority: 2]
[09:40-10:00] Fetch                (Max       ) due 10:00 (20 min) [priority: 2]
[10:00-10:30] Groom                (Buddy     ) due 11:00 (30 min) [priority: 1]
[10:30-11:00] Groom                (Mittens   ) due 11:00 (30 min) [priority: 1]
[12:00-12:30] Walk                 (Buddy     ) due 12:30 (30 min) [priority: 3]

============================================================
CONFLICT DETECTION DEMO
============================================================

Scenario 1: No Conflict (same breed, same task)
------------------------------------------------------------
Buddy (Dog) and Max (Dog) both performing Fetch at 10:00
OK: No conflicts detected

Tasks in Scenario 1:
  10:00 — Fetch (Buddy) (20 min) [priority: 2] [pending]
  10:00 — Fetch (Max) (20 min) [priority: 2] [pending]

Scenario 2: Conflict (different breeds, same task)
------------------------------------------------------------
Buddy (Dog) and Mittens (Cat) both performing Groom at 11:00
OK: No conflicts detected

Tasks in Scenario 2:
  11:00 — Groom (Buddy) (30 min) [priority: 1] [pending]
  11:00 — Groom (Mittens) (30 min) [priority: 1] [pending]
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

Confidence Level: 4 stars - all tests pass, not 100% if every possible edge case has been handled or super complex conflicts have been able to be resolved

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

1. Enter the owner's name at the top of the page.
2. Add one or more pets by entering a name and selecting a type (dog, cat, other).
3. Select a pet from the dropdown and add a task with a title, duration, priority, and due time.
4. Repeat step 3 for each task you want to schedule.
5. Click **Generate schedule** to see today's plan sorted by time and priority, along with any conflict warnings.

## ✨ Features

### Scheduling Algorithms
- **Backwards deadline scheduling** — Tasks are placed as late as possible relative to their due time, minimizing how early the owner has to start. The scheduler works backwards from each deadline so no task misses its window.
- **Priority-based ordering** — Within the same time window, tasks are sorted by priority (High → Medium → Low), ensuring the most important care happens first.
- **Parallel execution for same-breed pets** — If two pets of the same type share the same task and due time (e.g., two Dogs both due for Fetch at 10:00), the scheduler runs them simultaneously rather than sequencing them unnecessarily.
- **Sequential scheduling for different breeds** — Tasks for pets of different types (e.g., a Dog and a Cat both due for Groom at 11:00) are automatically spaced back-to-back so the owner can complete each one without overlap.
- **Earliest start time calculation** — After building the schedule, the scheduler surfaces the exact time the owner must begin to complete every task by its deadline.

### Task Management
- **Daily and weekly recurrence** — Marking a recurring task complete automatically creates the next occurrence for the following day or week, keeping the schedule current without manual re-entry.
- **Due time as a hard constraint** — Every scheduled task is guaranteed to finish by its due time. The schedule shifts earlier if needed to satisfy all deadlines.
- **Status tracking** — Tasks carry a status (pending / complete) that filters them in and out of the active schedule.

### Conflict Detection
- **Overlap detection** — The scheduler checks actual scheduled time slots (not just due times) and warns the owner when two incompatible tasks overlap.
- **Smart conflict rules** — Same task + same breed at the same time is allowed (parallel is fine). Same task + different breeds, or different tasks at the same time, are flagged as conflicts with a human-readable warning and recommended fixes.

### Filtering
- **By status** — View only pending or only completed tasks.
- **By pet** — Narrow the task list to a single pet's workload.
