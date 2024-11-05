import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title("Schedule Management Web App")

# Sidebar for adding new tasks
st.sidebar.header("Add New Task")

# Input fields for the task
task_name = st.sidebar.text_input("Task Name")
task_date = st.sidebar.date_input("Date")
task_time = st.sidebar.time_input("Time")
task_priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])

# Initialize session state for tasks if not already initialized
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["Task Name", "Date", "Time", "Priority"])

# Button to add the task
if st.sidebar.button("Add Task"):
    # Validate input to ensure task name is provided
    if not task_name.strip():
        st.error("Please enter a task name.")
    else:
        # Create a new task dictionary and append it to the DataFrame in session state
        new_task = {
            "Task Name": task_name,
            "Date": task_date,
            "Time": task_time,
            "Priority": task_priority
        }
        st.session_state.tasks = pd.concat(
            [st.session_state.tasks, pd.DataFrame([new_task])],
            ignore_index=True
        )
        st.success("Task added successfully!")

# Display the tasks
st.subheader("Scheduled Tasks")
st.dataframe(st.session_state.tasks)

# Function to save tasks to a CSV file
def save_tasks():
    st.session_state.tasks.to_csv("tasks.csv", index=False)

# Load tasks from CSV if the file exists
try:
    st.session_state.tasks = pd.read_csv("tasks.csv")
except FileNotFoundError:
    pass

# Button to save tasks to a file
if st.sidebar.button("Save Tasks"):
    save_tasks()
    st.success("Tasks saved to file!")
