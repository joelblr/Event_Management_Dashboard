import streamlit as st
from . import logics
import os



def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def login_validation():

    users = logics.load_user_data()

    local_id = st.session_state["login_local"]
    user_email = local_id + st.session_state["email_domain"]
    password1 = st.session_state["login_passwd1"]

    if logics.validate_email(user_email):
        if logics.validate_password(password1):
            user = users.get(user_email)
            if user and logics.check_password(password1, user["hashed_password"]):
                st.session_state["usr_email"] = user_email
                st.session_state["KEY"] = password1
                # initialize_session_state_for_user()
                print(f"INFO: @{st.session_state['get-DT']()} | Account: {user_email} logged-IN successfully!")
                st.success("Login successful!")
                st.toast("Login successful! 🎉")
                st.snow()
                # st.rerun()
                # st.experimental_rerun()
                # st.experimental_redirect("/")
            else:
                st.error("Incorrect email or password.")
        else:
            st.error("Password did not meet certain criteria, Check the help icon for info.")
    else:
        st.error("Invalid Email.")


def run():
                                        ## FIXME: True
    with st.form("login_form", clear_on_submit=False):
        st.subheader("Welcome back! Please log in to access your account.")
        logics.login_signup_component("login")
        submitted = st.form_submit_button(label="Login", on_click=login_validation)
