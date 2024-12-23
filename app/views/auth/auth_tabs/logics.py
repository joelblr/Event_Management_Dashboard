import re

def validate_email(email):
    """
    Validates an email address based on the following rules:
    1. The domain must be "caafrwsb.com".
    2. The local part (username) must:
        - Start with a letter.
        - Contain only alphanumeric characters, periods, underscores, and hyphens.
        - Be between 8 and 32 characters.
    3. The email must not exceed 45 characters.
    4. Prevent injection attacks by checking for unusual characters.

    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # Check overall length of the email 8+13=21, 32+13=45
    if len(email) > 45:
        # return False, 400
        return False

    if len(email) < 14:
        # return False, 401
        return False

    # Define the regex for the email format
    pattern = re.compile(r"""
        ^([a-zA-Z][a-zA-Z0-9._-]{4,45})   # Local part: starts with a letter, allows certain characters
        @                                  # @ symbol
        (gmail\.com)$                 # Domain must be "caafrwsb.com"
    """, re.VERBOSE)

    # Check if the email matches the regex
    if not pattern.match(email):
        # return False, 402
        return False

    # Additional security checks: Prevent injections or unsafe characters
    if any(char in email for char in ['\n', '\r', '\t', '\0', '\x0b', '\x0c']):
        # return False, 403
        return False

    # return True, 200
    return True


def validate_password(password):
    # Password validation regular expression
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*-]{8,20}$'

    if re.match(pattern, password):
        return True
        # return "Password is valid.", 200
    return False
        # ("Password must meet the following criteria:\n"
        #         "- At least one uppercase letter.\n"
        #         "- At least one lowercase letter.\n"
        #         "- At least one digit.\n"
        #         "- At least one special character (e.g., !@#$%^&*).\n"
        #         "- Length should be between 8 and 20 characters.\n"
        #         "- No spaces are allowed.")



# --------------------------------------------------------------------------------
import streamlit as st
import bcrypt, json, os



USER_DATA_FILE = os.path.join(st.session_state["cache_dr"], "user_data.json")
# ADMIN_IDS = ["joelblr", "katrathik", "kattanavya18", "kavacin"]


# Helper functions for JSON
def load_user_data():
    os.makedirs(st.session_state["cache_dr"], exist_ok=True)
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def login_signup_component(compo_type):
    """ type: login or signup"""

    autocomplete_type = "password"
    if compo_type == "signup":
        autocomplete_type = "off"

    # st.selectbox("Select your Role", options=["User", "Admin"],
    # help="Choose the role, Admin role will need verification.", key=f"{compo_type}_role")

    # Create two columns
    col1, col2 = st.columns([3, 2])

    # First column for the user input
    with col1:
        st.text_input(
            label='Enter your Email', max_chars=32,
            help="Start with a Letter\n\nOnly Letters, Numbers, Periods, Underscores, Hyphens\n\n8-32 Word Limit.",
            # autocomplete=autocomplete_type,  ##FIXME: OFF for sign-up
            key=f"{compo_type}_local",
        )
    msg = "Enter your" +(" new " if compo_type == "signup" else " ")+ "Password"
    st.text_input(
        label=msg, max_chars=20,
        help="At least 1 uppercase, 1 lowercase, 1 digit, 1 special char (!@#$%^&*)\n\n8-20 Word Limit\n\nNo Spaces.",
        type="password",
        # autocomplete="off",  ##FIXME- new-password, or password or off
        key=f"{compo_type}_passwd1",
    )
    if compo_type == "signup":
        st.text_input(
            label='Confirm new password', max_chars=20,
            help="At least 1 uppercase, 1 lowercase, 1 digit, 1 special char (!@#$%^&*)\n\n8-20 Word Limit\n\nNo Spaces.",
            type="password",
            #  autocomplete="off",  ##FIXME- new-password, or password or off
            key=f"{compo_type}_passwd2",
        )

    with col2:
        st.text_input(
            label="domain", value=st.session_state["email_domain"], disabled=True,label_visibility="hidden",
            key=f"{compo_type}_domain",
        )
