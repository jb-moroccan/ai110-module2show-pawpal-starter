# Scheduling Improvements: Daily vs Weekly Task Handling

## Problem Statement
The original scheduler did not account for:
1. Task duration affecting when tasks need to start
2. The difference between due time and actual schedule time
3. Whether daily vs weekly tasks should be excluded based on conflicts

## Solution: Three Key Improvements

### 1. Earliest Start Time Calculation (`pawpal_system.py`)

**Change**: Added `earliest_start_time` tracking to `Scheduler` class

```python
def build_schedule(self, owner: Owner) -> List[Task]:
    # ... existing code ...
    self.earliest_start_time = next_start if scheduled else None
```

**New Methods**:
- `get_earliest_start_time()` → Returns the datetime when owner must start
- `get_earliest_start_time_str()` → Returns formatted time (e.g., "07:45")

**Benefit**: Owner knows they need to start at 7:45 AM to complete a 5 PM deadline, not wait until 4:59 PM.

### 2. Intelligent Conflict Detection (`pawpal_system.py`)

**Change**: `detect_conflicts()` now checks actual scheduled times, not just due times

**Before**:
```python
if task1.due_datetime() != task2.due_datetime():
    continue  # Report conflict if due times match
```

**After**:
```python
task1_start = getattr(task1, "scheduled_start", task1.due_datetime())
task1_end = getattr(task1, "scheduled_end", task1.due_datetime())
# ... check if they actually overlap ...
if task1_end <= task2_start or task2_end <= task1_start:
    continue  # No conflict if scheduled at different times
```

**Benefit**: Tasks scheduled sequentially (9:00-9:30, then 9:30-10:00) don't report as conflicting even if both are "due at 10:00".

### 3. No Task Exclusion Based on Recurrence

**Key Decision**: Daily and weekly tasks are NOT excluded from the schedule.

- Both task types are scheduled together
- Conflicts are resolved by sequential scheduling, not deletion
- All tasks complete by their due times

**Example**:
```
07:45-08:00  Feed (daily) - due 08:00
08:45-09:30  Groom (weekly) - due 10:00
09:30-10:00  Groom other pet (weekly) - due 10:00
10:30-11:00  Walk (daily) - due 11:00
```

Both Groom tasks execute; they're just scheduled back-to-back.

## Test Coverage

Added three new tests in `tests/test_pawpal.py`:

1. `test_detect_conflicts_uses_scheduled_times_not_due_times()` 
   - Verifies tasks with same due time don't conflict if scheduled separately

2. `test_mixed_daily_and_weekly_tasks_scheduled_without_conflict()`
   - Confirms daily and weekly tasks coexist without exclusion

3. `test_build_schedule_excludes_conflicting_same_time_tasks_for_different_breeds()`
   - Ensures different pet types with same task are scheduled sequentially

## API Changes

### `Scheduler` class
- New attribute: `earliest_start_time: Optional[datetime]` (set by `build_schedule()`)
- New method: `get_earliest_start_time() -> Optional[datetime]`
- New method: `get_earliest_start_time_str() -> str`
- Updated method: `explain_schedule()` now shows scheduled times and earliest start

### `Task` class
- Dynamic attributes added by scheduler:
  - `scheduled_start: datetime` (when task actually runs)
  - `scheduled_end: datetime` (when task finishes)

## Usage Example

```python
scheduler = Scheduler()
# Add daily and weekly tasks...
schedule = scheduler.build_schedule(owner)

print(f"Start at: {scheduler.get_earliest_start_time_str()}")  # "07:45"
print(scheduler.explain_schedule())
# Output:
# Owner must start at 07:45 to complete all tasks on time.
# 
# Feed (priority 1, duration 15 min) - scheduled 07:45-08:00, due 08:00
# Walk (priority 3, duration 30 min) - scheduled 10:30-11:00, due 11:00
```

## Behavior Notes

- Tasks are scheduled backwards from deadlines
- Sequential scheduling prevents overlaps
- Daily and weekly tasks do NOT exclude each other
- Conflicts only occur if actual time slots overlap
- Owner gets one clear start time that ensures all tasks complete on time
