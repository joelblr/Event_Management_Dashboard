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
css_files = ["popover.css", "details.css"]
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


def form_component(key, name_val=None, email_val=None):
    with st.form(key=key, clear_on_submit=True, enter_to_submit=True):
        st.markdown("#### Enter Details to create an Attendee.")
        ename = st.text_input(label="Edit Attendee Name", help="Edit Attendee Name", max_chars=100,
            value=name_val)

        email = st.text_input(label="Edit Attendee Email", help="Edit Attendee Email", max_chars=100,
            value=email_val)

        submit = st.form_submit_button(label="Submit", help="Click to Update Attendee",
                on_click=None, args=None, kwargs=None,
                type="secondary", icon=None, disabled=False, use_container_width=False)
        if submit:
            update_to_attendees(key, ename, email)


def fetch_attendees():
    with st.spinner(f"Fetching Attendees from Database ... Plz wait"):
        try:
            url = f"{SERVER_URL}/attendees/"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.session_state["attendees"] = data.get("response")

            else:
                # Fetch error message from response.json() or response.text
                error_message = response.json().get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


def initialize_session_state(forced=False):
    """Initialize session state variables."""
    # st.session_state["popup"] = DialogPop(st)
    session_defaults = {
        "to_del": [],
        "attendees": {},
    }
    for key, default in session_defaults.items():
        if forced or (key not in st.session_state):
            st.session_state[key] = default




def update_to_attendees(key, ename, email):
    with st.spinner(f"Updating your Attendee to Database... Plz wait"):
        try:

            post_data = {
                "name": ename,
                "email": email,
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{SERVER_URL}/attendees/{key}"
            response = requests.put(url, json=post_data, headers=headers)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
                # fetch_attendees()
            else:
                # Fetch error message from response.json() or response.text
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔") 


def remove_from_attendees(eid):
    with st.spinner(f"Adding your Attendee to Database... Plz wait"):
        try:
            url = f"{SERVER_URL}/attendees/{eid}"
            response = requests.delete(url)
            data = response.json()

            if response.status_code in [200, 201]:
                del st.session_state["attendees"][eid]
                st.session_state["to_del"].append(eid)
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
                # fetch_attendees()
            else:
                # Fetch error message from response.json() or response.text
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


def add_to_attendees(ename, email):
    with st.spinner(f"Adding your Attendee to Database... Plz wait"):
        try:

            post_data = {
                "email": email,
                "name": ename,
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{SERVER_URL}/attendees/"
            response = requests.post(url, json=post_data, headers=headers)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
                # fetch_attendees()
            else:
                # Fetch error message from response.json() or response.text
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")



def create_attendee_component():
    # Define custom CSS for the table
    for key in st.session_state["attendees"]:
        cols = st.columns([8, 1, 1])
        with cols[0]:
            # cols[0].text("")
            with st.expander(label=f"Attendee: {key}", expanded=False, icon="🛠️"):
                # Convert the dictionary to a DataFrame with custom column names
                attendee_data = pd.DataFrame(
                    list(st.session_state["attendees"][key].items()),
                    columns=["Attribute", "Value"]  # Custom column names
                )

                # Render the DataFrame as an HTML table with the custom CSS
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
                for _, row in attendee_data.iterrows():
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
            # cols[1].text("")
            with st.popover("", icon="✏️"):
                form_component(key,
                name_val=st.session_state["attendees"][key]["name"],
                email_val=st.session_state["attendees"][key]["email"],
                )
        with cols[2]:
            with st.popover(label="", icon="🗑️"):
                with st.form(key=f"del-{key}", clear_on_submit=True, enter_to_submit=True):
                    st.markdown(f"#### Warning ⚠️ You will lose this Attendee Forever.\n##### Type `sudo rm -rf {key}` to confirm")
                    eid_txt = st.text_input("", max_chars=100)
                    confirm = st.form_submit_button(label="Confirm", help="Click to Create Attendee",
                    on_click=None, args=None, kwargs=None,
                    type="secondary", icon=None, disabled=False, use_container_width=False)

                    if confirm:
                        if eid_txt == f"sudo rm -rf {key}":
                            remove_from_attendees(key)
                        else:
                            st.toast(f"Wrong command to Delete Attendees", icon="⛔")





st.markdown(
    "<h1 style='text-align: center; color: #0D6EFD;'>Attendee Management Page</h1>",
    unsafe_allow_html=True
)


def show_create_btn():
    with st.popover(label="", help="Create a New Attendee",
        icon="➕", disabled=False, use_container_width=False,):
    # with st.popover(label="Create New Attendee", help="Create a New Attendee",
    #     icon="➕", disabled=False, use_container_width=True):
        with st.form(key="key", clear_on_submit=True, enter_to_submit=True):
            st.markdown("#### Enter Details to create an Attendee.")
            ename = st.text_input(label="Enter Attendee Name", help="Enter Attendee Name", max_chars=100)

            email = st.text_input(label="Enter Attendee Email", help="Enter Attendee Email", max_chars=100)

            submit = st.form_submit_button(label="Submit", help="Click to Create Attendee",
                on_click=None, args=None, kwargs=None,
                type="secondary", icon=None, disabled=False, use_container_width=False)

            if submit:
                add_to_attendees(ename, email)


initialize_session_state()
fetch_attendees()
show_create_btn()
create_attendee_component()