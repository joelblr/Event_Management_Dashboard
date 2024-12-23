import streamlit as st
import os, sys, json
import uuid
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from env_mgr import EnvMgr



def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


st.set_page_config(
    layout="centered"
)

st.session_state["styles_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "styles")
st.session_state["images_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "images")
st.session_state["get-DT"] = lambda: datetime.now().strftime("%d-%m-%Y -> %H:%M:%S")
st.session_state["cache_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "cache")


# Embed the Styles
css_styles = ""
css_files = ["side-nav-bar.css", "button.css", "logo.css", "material-icon.css"]#, "hide-header.css"]
for css_file in css_files:
    with open(os.path.join(st.session_state["styles_dr"], css_file)) as f:
        css = f.read()
    css_styles += f"{css}\n"
st.html(f"<style>{css_styles}</style>")


if "ROLE" not in st.session_state:
    st.session_state["ROLE"] = None

if "USER_ID" not in st.session_state:
    st.session_state["USER_ID"] = None

if "page_dict" not in st.session_state:
    st.session_state["page_dict"] = {}


def logout():
    role = st.session_state["ROLE"]
    user_email = st.session_state["USER_ID"]
    st.session_state["ROLE"] = None
    st.session_state["USER_ID"] = None
    st.session_state["page_dict"] = {}
    print(f"INFO: @{st.session_state['get-DT']()} | Account: {user_email} Logged-OUT successfully as {role}!")
    st.rerun()


# Login-SignUp
login_signup_page = st.Page(
    page="../aauth/Auth.py", title="Home", icon="🔐", # url_path="/auth",
    # default=True,
)

# Account
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# About
home_page = st.Page(
    page="../about/Home.py", title="Home", icon="🏠", # url_path="/cool1",
    default=True,
)
docs_page = st.Page(
    page="../about/Docs.py", title="Documentation", icon="🚩", #url_path="/cool2",
)
contributors_page = st.Page(
    page="../about/Contributors.py", title="Contributors", icon="🎪"
)

# Products
caafr_page = st.Page(
    page="../products/CAAFR.py", title="CAAFR", icon="🚀"
)
wst_page = st.Page(
    page="../products/Scraper_Bot.py", title="Scraper Bot", icon="🔍"
)

# Admin
datasets_page = st.Page(
    page="../admin/Datasets.py", title="Datasets History", icon="📁"
)
llm_config_page = st.Page(
    page="../admin/LLM_Config.py", title="LLM Config", icon="🎃"
)
usr_hist_page = st.Page(
    page="../admin/Accounts.py", title="Accounts", icon="💼"
)
testing_page = st.Page(
    page="../admin/Testing.py", title="Testing", icon="🚧"
)


if "logo" not in st.session_state:
    st.session_state["logo"] = os.path.join(st.session_state["images_dr"], "pro_logo.webp")

st.logo(
    image=os.path.join(st.session_state["logo"]),
    link="https://github.com/joelblr/CAAFR",
    # icon_image=os.path.join(st.session_state["images_dr"], "pro_logo1.jpeg"),
)


if st.session_state["ROLE"] and st.session_state["USER_ID"]:
    st.session_state["page_dict"]["Account"] = [logout_page]
    st.session_state["page_dict"]["About"] = [home_page, docs_page, contributors_page]
    st.session_state["page_dict"]["Products"] = [caafr_page, wst_page]
    if st.session_state["ROLE"] == "Admin":
        st.session_state["page_dict"]["Admin"] = [usr_hist_page, datasets_page, llm_config_page, testing_page]


if len(st.session_state["page_dict"]) > 0:

    st.session_state["env_mgr"] = EnvMgr.EnvManager
    st.session_state["env_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "..", "env_mgr")
    st.session_state["scripts_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "scripts")
    st.session_state["pvt_db_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "database")
    st.session_state["pub_db_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database")
    st.session_state["views_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "views")
    st.session_state["docs_img_dr"] = os.path.join(os.path.dirname(__file__), "..", "..", "docs_img")

    st.session_state["usr_cache_dr"] = os.path.join(st.session_state["cache_dr"], st.session_state["USER_ID"])
    st.session_state["usr_db_dr"] = os.path.join(st.session_state["pvt_db_dr"], st.session_state["USER_ID"])
    create_directory_if_not_exists(os.path.join(st.session_state["usr_db_dr"], "azon"))
    create_directory_if_not_exists(os.path.join(st.session_state["usr_db_dr"], "fkart"))

    st.session_state["env_shared"] = st.session_state["env_mgr"](
        ".env.shared",
        st.session_state["env_dr"]
    )

    st.session_state["env_client"] = st.session_state["env_mgr"](
        ".env.client",
        st.session_state["usr_cache_dr"], st.session_state["env_dr"]
    ); st.session_state["env_client"].update_env_keys({
        "ROLE": st.session_state["ROLE"],
        "USER_ID": st.session_state["USER_ID"],
    })

    pg = st.navigation(st.session_state["page_dict"])
    # Inject dynamic CSS with a professional style
    st.session_state["USER_NAME"] = st.session_state['USER_ID'].split("@")[0]
    st.html(
    f"""
        <style>            
            [data-testid="stSidebarNav"]::before {{
                content: 'Welcome {st.session_state["USER_NAME"]}';
            }}
        </style>
    """)


else:
    pg = st.navigation([login_signup_page])

pg.run()
