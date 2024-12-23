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
        st.markdown("#### Enter Details to create an Event.")
        ename = st.text_input(label="Edit Event Name", help="Edit Event Name", max_chars=100,
            value=name_val)
        edesc = st.text_area(label="Edit Event Description",
            key=None, help="Edit Event Description", height=None, max_chars=500,
            on_change=None, args=None, kwargs=None,
            placeholder=None, disabled=False, label_visibility="visible",
            value=desc_val)

        eloc = st.text_input(label="Edit Event Location", help="Edit Event Location", max_chars=100,
            value=loc_val)

        edate = st.date_input(
            label="Select your Event Date",
            help="Select your Event Date",
            # (default_start, default_end),
            value=today if not date_val else date_val,
            # min_value=today,
            # max_value=five_years_later,
            format="YYYY-MM-DD",  # Date format
        )

        submit = st.form_submit_button(label="Submit", help="Click to Update Event",
                on_click=None, args=None, kwargs=None,
                type="secondary", icon=None, disabled=False, use_container_width=False)
        if submit:
            update_to_events(key, ename, edesc, eloc, edate)

        # st.form_submit_button

def fetch_events():
    with st.spinner(f"Fetching Events from Database ... Plz wait"):
        try:
            url = f"{SERVER_URL}/events/"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.session_state["events"] = data.get("response")
                # st.toast("Successfully Fetched Events from DB. ", icon="🎉")
                # st.snow()
                # st.rerun()
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
        "events": {},
    }
    for key, default in session_defaults.items():
        if forced or (key not in st.session_state):
            st.session_state[key] = default

    # if "" not in st.session_state:

    #     fetch_events()



def update_to_events(eid, ename, edesc, eloc, edate):
    with st.spinner(f"Updating your Event to Database... Plz wait"):
        try:

            post_data = {
                "event_id": eid,
                "name": ename,
                "description": edesc,
                "location": eloc,
                "date": str(edate)
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{SERVER_URL}/events/{eid}"
            response = requests.put(url, json=post_data, headers=headers)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
                # fetch_events()
            else:
                # Fetch error message from response.json() or response.text
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔") 


def remove_from_events(eid):
    with st.spinner(f"Adding your Event to Database... Plz wait"):
        try:
            url = f"{SERVER_URL}/events/{eid}"
            response = requests.delete(url)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                del st.session_state["events"][eid]
                st.session_state["to_del"].append(eid)
                st.snow()
                st.rerun()
                # fetch_events()
            else:
                # Fetch error message from response.json() or response.text
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")


def add_to_events(eid, ename, edesc, eloc, edate):
    with st.spinner(f"Adding your Event to Database... Plz wait"):
        try:

            post_data = {
                "event_id": eid,
                "name": ename,
                "description": edesc,
                "location": eloc,
                "date": str(edate)
            }

            headers = {'Content-Type': 'application/json'}
            url = f"{SERVER_URL}/events/"
            response = requests.post(url, json=post_data, headers=headers)
            data = response.json()

            if response.status_code in [200, 201]:
                st.toast(data.get("message"), icon="🎉")
                st.snow()
                st.rerun()
                # fetch_events()
            else:
                # Fetch error message from response.json() or response.text
                error_message = data.get('error', 'An error occurred')
                st.error(f"{response.status_code} ERROR: {error_message}")
                st.toast(f"{response.status_code} ERROR: {error_message}", icon="⛔")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.toast(f"Error fetching data", icon="⛔")



def create_event_component():
    # Define custom CSS for the table
    for key in st.session_state["events"]:
        cols = st.columns([8, 1, 1])
        with cols[0]:
            # cols[0].text("")
            with st.expander(label=f"Event #{key[4:]}", expanded=False, icon="📌"):
                # Convert the dictionary to a DataFrame with custom column names
                event_data = pd.DataFrame(
                    list(st.session_state["events"][key].items()),
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
                for _, row in event_data.iterrows():
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
                name_val=st.session_state["events"][key]["name"],
                desc_val=st.session_state["events"][key]["description"],
                loc_val=st.session_state["events"][key]["location"],
                date_val=st.session_state["events"][key]["date"])
        with cols[2]:
            with st.popover(label="", icon="🗑️"):
                with st.form(key=f"del-{key}", clear_on_submit=True, enter_to_submit=True):
                    st.markdown(f"#### Warning ⚠️ You will lose this Event Forever.\n##### Type `sudo rm -rf {key}` to confirm")
                    eid_txt = st.text_input("", max_chars=100)
                    confirm = st.form_submit_button(label="Confirm", help="Click to Create Event",
                    on_click=None, args=None, kwargs=None,
                    type="secondary", icon=None, disabled=False, use_container_width=False)

                    if confirm:
                        if eid_txt == f"sudo rm -rf {key}":
                            remove_from_events(key)
                        else:
                            st.toast(f"Wrong command to Delete Events", icon="⛔")





st.markdown(
    "<h1 style='text-align: center; color: #0D6EFD;'>Event Management Page</h1>",
    unsafe_allow_html=True
)


def show_create_btn():
    with st.popover(label="", help="Create a New Event",
        icon="➕", disabled=False, use_container_width=False,):
    # with st.popover(label="Create New Event", help="Create a New Event",
    #     icon="➕", disabled=False, use_container_width=True):
        with st.form(key="key", clear_on_submit=True, enter_to_submit=True):
            st.markdown("#### Enter Details to create an Event.")
            ename = st.text_input(label="Enter Event Name", help="Enter Event Name", max_chars=100)
            edesc = st.text_area(label="Enter Event Description", value="",
                key=None, help="Enter Event Description", height=None, max_chars=500,
                on_change=None, args=None, kwargs=None,
                placeholder=None, disabled=False, label_visibility="visible")

            eloc = st.text_input(label="Enter Event Location", help="Enter Event Location", max_chars=100)

            edate = st.date_input(
                label="Select your Event Date",
                help="Select your Event Date",
                # (default_start, default_end),
                value=today,
                min_value=today,
                max_value=five_years_later,
                format="YYYY-MM-DD",  # Date format
            )

            submit = st.form_submit_button(label="Submit", help="Click to Create Event",
                on_click=None, args=None, kwargs=None,
                type="secondary", icon=None, disabled=False, use_container_width=False)

            if submit:
                add_to_events(get_uid("eid"), ename, edesc, eloc, edate)


initialize_session_state()
fetch_events()
show_create_btn()
create_event_component()