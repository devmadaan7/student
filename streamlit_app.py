import streamlit as st
import pandas as pd
from datetime import datetime, date

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
    st.session_state.tasks = pd.DataFrame(columns=["Task Name", "Date", "Time", "Priority", "Completed"])

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
    # Convert 'Completed' column to boolean if necessary
    st.session_state.tasks["Completed"] = st.session_state.tasks["Completed"].astype(bool)
except FileNotFoundError:
    pass

# Display the tasks with checkboxes
st.subheader("Scheduled Tasks")
for index, task in st.session_state.tasks.iterrows():
    completed = st.checkbox(
        f"{task['Task Name']} (Due: {task['Date']}, {task['Time']}, Priority: {task['Priority']})",
        task["Completed"],
        key=f"task_{index}"
    )
    st.session_state.tasks.at[index, "Completed"] = completed

# Daily summary: Important tasks missed today
st.subheader("Daily Summary")
today = date.today()
missed_tasks = st.session_state.tasks[
    (st.session_state.tasks["Date"] == str(today)) & 
    (st.session_state.tasks["Priority"] == "High") & 
    (~st.session_state.tasks["Completed"])
]

if not missed_tasks.empty:
    st.warning("You have missed the following important tasks today:")
    st.dataframe(missed_tasks)
else:
    st.success("Great job! You have completed all your important tasks today.")

# Button to save tasks to a file
if st.sidebar.button("Save Tasks"):
    save_tasks()
    st.success("Tasks saved to file!")
