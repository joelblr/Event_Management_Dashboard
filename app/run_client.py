import streamlit as st
import os, sys, json
# import uuid
from datetime import datetime


st.set_page_config(
    layout="centered"
)

st.session_state["views_dr"] = os.path.join(os.path.dirname(__file__), "views")
st.session_state["styles_dr"] = os.path.join(os.path.dirname(__file__), "styles")
st.session_state["images_dr"] = os.path.join(os.path.dirname(__file__), "images")
st.session_state["scripts_dr"] = os.path.join(os.path.dirname(__file__), "scripts")

st.session_state["get-DT"] = lambda: datetime.now().strftime("%d-%m-%Y -> %H:%M:%S")


# Embed the Styles
css_styles = ""
css_files =  ["auth.css", "login.css", "side-nav-bar.css", "button.css", "logo.css", "material-icon.css"]#, "hide-header.css"]
for css_file in css_files:
    with open(os.path.join(st.session_state["styles_dr"], css_file)) as f:
        css = f.read()
    css_styles += f"{css}\n"
st.html(f"<style>{css_styles}</style>")

if "usr_email" not in st.session_state:
    st.session_state["usr_email"] = None
    st.session_state["usr_email"] = "joelblr@gmail.com"

if "page_dict" not in st.session_state:
    st.session_state["page_dict"] = {}


def logout():
    usr_email = st.session_state["usr_email"]
    st.session_state["usr_email"] = None
    st.session_state["page_dict"] = {}
    st.toast(f"Account: {usr_email} Logged-OUT successfully 🎉", icon="✔️")
    print(f"INFO: @{st.session_state["get-DT"]()} | Account: {usr_email} Logged-OUT successfully!")
    st.rerun()


# # Login-SignUp
# login_signup_page = st.Page(
#     page="run_client.py", title="Home", icon="🔐", # url_path="/auth",
#     # page="../views/auth/Auth.py", title="Home", icon="🔐", # url_path="/auth",
#     # default=True,
# )

# Account
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# About
home_page = st.Page(
    page="./views/Home.py", title="Home", icon="🏠", # url_path="/cool1",
    default=True,
)

# Products
events_page = st.Page(
    page="./views/Events.py", title="Events", icon="🚩", #url_path="/cool2",
)

attendees_page = st.Page(
    page="./views/Attendees.py", title="Attendees", icon="🎪"
)

tasks_page = st.Page(
    page="./views/Tasks.py", title="Tasks", icon="🚀"
)


if "logo" not in st.session_state:
    st.session_state["logo"] = os.path.join(st.session_state["images_dr"], "logo.jpg")

st.logo(
    image=os.path.join(st.session_state["logo"]),
    link="https://github.com/joelblr/Event_Management_Dashboard",
)


if st.session_state["usr_email"]:
    st.session_state["page_dict"]["Account"] = [logout_page]
    st.session_state["page_dict"]["About"] = [home_page]
    st.session_state["page_dict"]["Products"] = [events_page, attendees_page, tasks_page]

if len(st.session_state["page_dict"]) > 0:

    pg = st.navigation(st.session_state["page_dict"])
    # Inject dynamic CSS with a professional style
    st.session_state["usr_name"] = st.session_state['usr_email'].split("@")[0]
    st.html(
    f"""
        <style>            
            [data-testid="stSidebarNav"]::before {{
                content: 'Welcome {st.session_state["usr_name"]}';
            }}
        </style>
    """)


else:
    pg = st.navigation([login_signup_page])

pg.run()



# import streamlit as st

# if "server_runs" not in st.session_state:
#     st.session_state.server_runs = 0
#     st.session_state.fragment_runs = 0


# @st.fragment
# def my_fragment():
#     st.session_state.fragment_runs += 1
#     st.button("Rerun fragment")
#     st.write(f"Fragment says it ran {st.session_state.fragment_runs} times.")


# st.session_state.server_runs += 1
# my_fragment()
# st.button("Rerun full server")
# st.write(f"Full server says it ran {st.session_state.server_runs} times.")
# st.write(f"Full server sees that fragment ran {st.session_state.fragment_runs} times.")

