import streamlit as st
from . import logics
import os



def signup_validation():

    users = logics.load_user_data()

    # role = st.session_state["signup_role"]
    local_id = st.session_state["signup_local"]
    user_email = local_id + st.session_state["email_domain"]
    password1 = st.session_state["signup_passwd1"]
    password2 = st.session_state["signup_passwd2"]

    if logics.validate_email(user_email):
        if user_email not in users:
            if logics.validate_password(password1):
                if password1 == password2:
                    hashed_password = str(logics.hash_password(password1))[2:-1]
                    users[user_email] = {
                        "hashed_password": hashed_password,
                    }
                    logics.save_user_data(users)
                    print(f"Account: {user_email} registered successfully!")
                    st.success(f"Account registered successfully!")
                else:
                    st.error("Passwords do not match.")
            else:
                st.error("Password did not meet certain criteria, Check the help icon for info.")
        else:
            st.error("Email already exists.")
    else:
        st.error("Invalid Email.")


def run():
                                            ## FIXME: True
    with st.form("signup_form", clear_on_submit=False):
        st.subheader("Create an account to get started.")
        logics.login_signup_component("signup")
        submitted = st.form_submit_button(label="Sign Up", on_click=signup_validation)
