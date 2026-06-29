import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

owner_name = st.text_input("Owner name", value=owner.name)

if owner_name != owner.name:
    owner.set_name(owner_name)
    st.session_state.owner = owner

st.markdown("### Add a Pet")
st.caption("Use the form below to add a pet to the current owner.")

pet_name_input = st.text_input("Pet name", key="pet_name_input", value="")
pet_type_input = st.selectbox("Pet type", ["dog", "cat", "other"], key="pet_type_input")

if st.button("Add pet"):
    if pet_name_input.strip():
        new_pet = Pet(name=pet_name_input.strip(), type=pet_type_input)
        owner.add_pet(new_pet)
        st.session_state.owner = owner
        st.success(f"Added {new_pet.name} to {owner.name or 'the owner profile'}.")
    else:
        st.warning("Please enter a pet name first.")

if owner.pets:
    st.write("Current pets:")
    pet_rows = [{"name": pet.name, "type": pet.type, "tasks": len(pet.tasks)} for pet in owner.pets]
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a task for one of your pets and send it to the scheduler.")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Assign task to pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")

    if st.button("Add task"):
        if task_title.strip():
            selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)
            if selected_pet is not None:
                priority_map = {"low": 3, "medium": 2, "high": 1}
                task = Task(
                    name=task_title.strip(),
                    priority=priority_map[priority],
                    duration_minutes=int(duration),
                    due_date="Today",
                )
                selected_pet.add_task(task)
                scheduler.add_task(task)
                st.session_state.owner = owner
                st.session_state.scheduler = scheduler
                st.success(f"Added '{task.name}' for {selected_pet.name}.")
            else:
                st.warning("Please select a valid pet.")
        else:
            st.warning("Please enter a task title first.")
else:
    st.info("Add a pet before creating tasks.")

all_tasks = [task for pet in owner.pets for task in pet.tasks]
if all_tasks:
    st.write("Current tasks:")
    task_rows = [
        {
            "task": task.name,
            "pet": next((pet.name for pet in owner.pets if task in pet.tasks), "Unknown"),
            "duration": task.duration_minutes,
            "priority": task.priority,
        }
        for task in all_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button uses the scheduler to build a plan from the current owner and pets.")

if st.button("Generate schedule"):
    schedule = scheduler.build_schedule(owner)
    st.write("Today's Schedule")
    for task in schedule:
        pet_name = next((pet.name for pet in owner.pets if task in pet.tasks), "Unknown")
        st.write(f"{task.due_date or ''} — {task.name} ({task.duration_minutes} min) [priority: {task.priority}]")
