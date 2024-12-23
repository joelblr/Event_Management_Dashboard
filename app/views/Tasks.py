from datetime import datetime, timedelta
import streamlit as st
import requests
import pandas as pd
import os, uuid


SERVER_URL = "http://127.0.0.1:5000"

# Current date
today = datetime.now().date()
# Calculate the date 5 years from today
five_years_later = today + timedelta(days=5*365)
# Default range: Today to a week later
default_start = today
default_end = today + timedelta(days=7)

# Embed the Styles
css_styles = ""
css_files = ["details.css", "popover.css"]
for css_file in css_files:
    with open(os.path.join(st.session_state["styles_dr"], css_file)) as f:
        css = f.read()
    css_styles += f"{css}\n"
st.html(f"<style>{css_styles} </style>")

table_style = ""
with open(os.path.join(st.session_state["styles_dr"], "table.css")) as f:
    table_style = "<style>" + f.read() + "</style>"


def get_uid(prefix=""):
    return prefix + "_" + str(uuid.uuid4())


def form_component(key, name_val=None, desc_val=None, loc_val=None, date_val=None):
    with st.form(key=key, clear_on_submit=True, enter_to_submit=True):
        st.markdown("#### Enter Details to create a Task.")
        ename = st.text_input(label="Edit Task Name", help="Edit Task Name", max_chars=100,
            value=name_val)
        edesc = st.text_area(label="Edit Task Description",
            key=None, help="Edit Task Description", height=None, max_chars=500,
            on_change=None, args=None, kwargs=None,
            placeholder=None, disabled=False, label_visibility="visible",
            value=desc_val)

        eloc = st.text_input(label="Edit Task Location", help="Edit Task Location", max_chars=100,
            value=loc_val)

        edate = st.date_input(
            label="Select your Task Date",
            help="Select your Task Date",
            # (default_start, default_end),
            value=today if not date_val else date_val,
            # min_value=today,
            # max_value=five_years_later,
            format="YYYY-MM-DD",  # Date format
        )

        submit = st.form_submit_button(label="Submit", help="Click to Update Task",
                on_click=None, args=None, kwargs=None,
                type="secondary", icon=None, disabled=False, use_container_width=False)
        if submit:
            update_to_tasks(key, ename, edesc, eloc, edate)


def fetch_tasks():
    with st.spinner(f"Fetching Tasks from Database ... Plz wait"):
        try:
            url = f"{SERVER_URL}/tasks/"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.session_state["tasks"] = data.get("response")
            else:
                error_message = response.json().get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


def initialize_session_state(forced=False):
    session_defaults = {
        "to_del": [],
        "tasks": {},
    }
    for key, default in session_defaults.items():
        if forced or (key not in st.session_state):
            st.session_state[key] = default


def update_to_tasks(eid, ename, edesc, eloc, edate):
    with st.spinner(f"Updating your Task to Database... Plz wait"):
        try:

            post_data = {
                "task_id": eid,
                "name": ename,
                "description": edesc,
                "location": eloc,
                "date": str(edate)
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{SERVER_URL}/tasks/{eid}"
            response = requests.put(url, json=post_data, headers=headers)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
            else:
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


# Similar updates for other functions like `remove_from_tasks`, `add_to_tasks`, and `create_task_component`.

# Update the heading
st.markdown(
    "<h1 style='text-align: center; color: #0D6EFD;'>Task Management Page</h1>",
    unsafe_allow_html=True
)


def remove_from_tasks(eid):
    with st.spinner(f"Removing your Task from Database... Plz wait"):
        try:
            url = f"{SERVER_URL}/tasks/{eid}"
            response = requests.delete(url)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                del st.session_state["tasks"][eid]
                st.session_state["to_del"].append(eid)
                st.snow()
                st.rerun()
            else:
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


def add_to_tasks(eid, ename, edesc, eloc, edate):
    with st.spinner(f"Adding your Task to Database... Plz wait"):
        try:

            post_data = {
                "task_id": eid,
                "name": ename,
                "description": edesc,
                "location": eloc,
                "date": str(edate)
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{SERVER_URL}/tasks/"
            response = requests.post(url, json=post_data, headers=headers)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
            else:
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


def create_task_component():
    for key in st.session_state["tasks"]:
        cols = st.columns([8, 1, 1])
        with cols[0]:
            with st.expander(label=f"Task #{key[4:]}", expanded=False, icon="📌"):
                task_data = pd.DataFrame(
                    list(st.session_state["tasks"][key].items()),
                    columns=["Attribute", "Value"]
                )

                table_html = f"""
                {table_style}
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Attribute</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for _, row in task_data.iterrows():
                    table_html += f"""
                    <tr>
                        <td><b>{row['Attribute'].capitalize()}</b></td>
                        <td>{row['Value']}</td>
                    </tr>
                    """
                table_html += """
                    </tbody>
                </table>
                """
                st.html(table_html)
        with cols[1]:
            with st.popover("", icon="✏️"):
                form_component(key,
                               name_val=st.session_state["tasks"][key]["name"],
                               desc_val=st.session_state["tasks"][key]["description"],
                               loc_val=st.session_state["tasks"][key]["location"],
                               date_val=st.session_state["tasks"][key]["date"])
        with cols[2]:
            with st.popover(label="", icon="🗑️"):
                with st.form(key=f"del-{key}", clear_on_submit=True, enter_to_submit=True):
                    st.markdown(f"#### Warning ⚠️ You will lose this Task Forever.\n##### Type `sudo rm -rf {key}` to confirm")
                    eid_txt = st.text_input("", max_chars=100)
                    confirm = st.form_submit_button(label="Confirm", help="Click to Delete Task",
                                                    type="secondary")
                    if confirm:
                        if eid_txt == f"sudo rm -rf {key}":
                            remove_from_tasks(key)
                        else:
                            st.toast(f"Wrong command to Delete Task", icon="⛔")


def show_create_btn():
    with st.popover(label="", help="Create a New Task",
                    icon="➕", disabled=False, use_container_width=False):
        with st.form(key="create_task", clear_on_submit=True, enter_to_submit=True):
            st.markdown("#### Enter Details to create a Task.")
            ename = st.text_input(label="Enter Task Name", help="Enter Task Name", max_chars=100)
            edesc = st.text_area(label="Enter Task Description", value="",
                                 key=None, help="Enter Task Description", height=None, max_chars=500)
            eloc = st.text_input(label="Enter Task Location", help="Enter Task Location", max_chars=100)
            edate = st.date_input(
                label="Select your Task Date",
                help="Select your Task Date",
                value=today,
                min_value=today,
                max_value=five_years_later,
                format="YYYY-MM-DD",
            )
            submit = st.form_submit_button(label="Submit", help="Click to Create Task",
                                           type="secondary")
            if submit:
                add_to_tasks(get_uid("tid"), ename, edesc, eloc, edate)


initialize_session_state()
fetch_tasks()
show_create_btn()
create_task_component()
