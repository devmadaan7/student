import streamlit as st
import pandas as pd
from datetime import date

# Title of the app
st.title("Schedule Management Web App")

# Sidebar for adding new tasks
st.sidebar.header("Add New Task")

# Input fields for the task
task_name = st.sidebar.text_input("Task Name")
task_date = st.sidebar.date_input("Date", min_value=date.today())  # Default to today, no past dates
task_time = st.sidebar.time_input("Time")
task_priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])

# Initialize session state for tasks if not already initialized
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(
        columns=["Task Name", "Date", "Time", "Priority", "Completed"]
    )

# Button to add the task
if st.sidebar.button("Add Task"):
    if not task_name.strip():
        st.error("Please enter a task name.")
    else:
        new_task = {
            "Task Name": task_name,
            "Date": task_date,
            "Time": task_time,
            "Priority": task_priority,
            "Completed": False  # New task is not completed by default
        }
        st.session_state.tasks = pd.concat(
            [st.session_state.tasks, pd.DataFrame([new_task])],
            ignore_index=True
        )
        st.success("Task added successfully!")

# Function to save tasks to a CSV file
def save_tasks():
    st.session_state.tasks.to_csv("tasks.csv", index=False)

# Load tasks from CSV if the file exists
try:
    st.session_state.tasks = pd.read_csv("tasks.csv")
    st.session_state.tasks["Completed"] = st.session_state.tasks["Completed"].astype(bool)
except FileNotFoundError:
    pass

# Display the tasks with checkboxes and options to edit/delete
st.subheader("Scheduled Tasks")
for index, task in st.session_state.tasks.iterrows():
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        completed = st.checkbox(
            f"{task['Task Name']} (Due: {task['Date']}, {task['Time']}, Priority: {task['Priority']})",
            task["Completed"],
            key=f"task_{index}"
        )
        st.session_state.tasks.at[index, "Completed"] = completed
    with col2:
        if st.button("Edit", key=f"edit_{index}"):
            # Edit the task (you can expand this as needed)
            st.session_state.edit_index = index
            st.session_state.edit_mode = True
    with col3:
        if st.button("Delete", key=f"delete_{index}"):
            st.session_state.tasks.drop(index, inplace=True)
            st.session_state.tasks.reset_index(drop=True, inplace=True)
            st.experimental_rerun()

# Handle task editing
if "edit_mode" in st.session_state and st.session_state.edit_mode:
    st.sidebar.subheader("Edit Task")
    edit_index = st.session_state.edit_index
    task_to_edit = st.session_state.tasks.loc[edit_index]
    new_name = st.sidebar.text_input("Task Name", task_to_edit["Task Name"])
    new_date = st.sidebar.date_input("Date", task_to_edit["Date"])
    new_time = st.sidebar.time_input("Time", task_to_edit["Time"])
    new_priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task_to_edit["Priority"]))
    
    if st.sidebar.button("Update Task"):
        st.session_state.tasks.at[edit_index, "Task Name"] = new_name
        st.session_state.tasks.at[edit_index, "Date"] = new_date
        st.session_state.tasks.at[edit_index, "Time"] = new_time
        st.session_state.tasks.at[edit_index, "Priority"] = new_priority
        st.session_state.edit_mode = False
        st.experimental_rerun()

# Task completion summary
st.subheader("Task Completion Summary")
total_tasks = len(st.session_state.tasks)
completed_tasks = st.session_state.tasks["Completed"].sum()
incomplete_tasks = total_tasks - completed_tasks

st.write(f"**Total Tasks:** {total_tasks}")
st.write(f"**Completed Tasks:** {completed_tasks}")
st.write(f"**Incomplete Tasks:** {incomplete_tasks}")

# Daily summary with task completion details
st.subheader("Daily Summary")
today = date.today()
today_tasks = st.session_state.tasks[st.session_state.tasks["Date"] == str(today)]

if not today_tasks.empty:
    completed_today = today_tasks["Completed"].sum()
    high_priority_today = today_tasks[today_tasks["Priority"] == "High"]
    missed_high_priority = high_priority_today[~high_priority_today["Completed"]]
    
    st.write(f"**Total Tasks Today:** {len(today_tasks)}")
    st.write(f"**Tasks Completed Today:** {completed_today}")
    
    if not missed_high_priority.empty:
        st.warning("You have missed the following important tasks today:")
        st.dataframe(missed_high_priority)
    else:
        st.success("Great job! You have completed all your important tasks today.")
else:
    st.info("No tasks scheduled for today.")

# Button to save tasks to a file
if st.sidebar.button("Save Tasks"):
    save_tasks()
    st.success("Tasks saved to file!")
