import streamlit as st

if "server_runs" not in st.session_state:
    st.session_state.server_runs = 0
    st.session_state.fragment_runs = 0


@st.fragment
def my_fragment():
    st.session_state.fragment_runs += 1
    st.button("Rerun fragment")
    st.write(f"Fragment says it ran {st.session_state.fragment_runs} times.")


st.session_state.server_runs += 1
my_fragment()
st.button("Rerun full server")
st.write(f"Full server says it ran {st.session_state.server_runs} times.")
st.write(f"Full server sees that fragment ran {st.session_state.fragment_runs} times.")

