from views.auth.auth_tabs import login_tab, signup_tab
import streamlit as st
from streamlit_option_menu import option_menu
import os



# USER_DATA_FILE = "user_data.json"
st.session_state["email_domain"] = "@gmail.com"
# ADMIN_IDS = ["joel022003"]


# Embed the Styles
css_styles = ""
css_files = ["auth.css"]
for css_file in css_files:
    with open(os.path.join(st.session_state["styles_dr"], css_file)) as f:
        css = f.read()
    css_styles += f"{css}\n"
st.html(f"<style>{css_styles}</style>")


if "tab_menu" not in st.session_state:
    st.session_state["tab_menu"] = "Login"


selected = option_menu(
    menu_title=None,
    options=["Login", "Sign Up"],
    icons=["box-arrow-in-right", "person-plus"],
    orientation="horizontal",
    default_index=(st.session_state["tab_menu"]=="Sign Up"),
    key="tab_menu",
    styles={
        "container": {
            "padding": "10px 20px", 
            "background-color": "#f8f9fa",
            "border-radius": "10px",  # Optional: for a rounded container
        },
        "nav-link": {
            "font-size": "20px",  # Adjust font size for text
            "margin": "0px",
            "color": "black",
            "font-weight": "bold",  # Optional: to make the text bolder
        },
        "nav-link-selected": {
            "background-color": "#007bff",
            "color": "white",
            "border-radius": "5px",  # Optional: to round the selected link
        },
        "icon": {
            "font-size": "24px",  # Increase icon size
            "margin-right": "8px",  # Optional: space between icon and text
        },
    }
)


mod_map = {
    "Login": login_tab,
    "Sign Up": signup_tab,
}

# Dynamically load and run the selected page, passing `st` or `st.session_state`
try:
    if st.session_state["usr_email"]:
        print("OOPS, Why Here...?")
        print(st.session_state["usr_email"])
    else:
        mod_map[selected].run()

except ModuleNotFoundError as e:
    st.error(f"Page not found: {selected}\n{e}")
# except Exception as e:
#     st.error(f"An unexpected error occurred: {e}")
