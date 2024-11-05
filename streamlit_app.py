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

# Button to add the task
if st.sidebar.button("Add Task"):
    # Save task to a dataframe (for demonstration, using in-memory storage)
    if "tasks" not in st.session_state:
        st.session_state.tasks = pd.DataFrame(columns=["Task Name", "Date", "Time", "Priority"])
    
    new_task = {"Task Name": task_name, "Date": task_date, "Time": task_time, "Priority": task_priority}
    st.session_state.tasks = st.session_state.tasks.append(new_task, ignore_index=True)
    st.success("Task added successfully!")

# Display the tasks
if "tasks" in st.session_state:
    st.subheader("Scheduled Tasks")
    st.dataframe(st.session_state.tasks)

