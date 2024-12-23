# import streamlit as st
# import os, sys, json
# # import uuid
# from datetime import datetime


# # Embed the Styles
# css_styles = ""
# css_files = ["login.css"]
# for css_file in css_files:
#     with open(os.path.join(st.session_state["styles_dr"], css_file)) as f:
#         css = f.read()
#     css_styles += f"{css}\n"
# # st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
# st.html(f"<style>{css_styles}</style>")

# st.markdown(
#     "<h1 style='text-align: center; color: #0D6EFD;'>Home</h1>",
#     unsafe_allow_html=True
# )

#------------------------------------------------------------
# import streamlit as st
# from streamlit_extras.switch_page_button import switch_page
# from PIL import Image

# # Custom CSS for styling
# def apply_custom_styles():
#     st.markdown(
#         """
#         <style>
#         .main-header {
#             font-family: 'Arial', sans-serif;
#             color: #0F9DDA;
#             text-align: center;
#             font-size: 2.5rem;
#             margin-bottom: 1rem;
#         }
#         .sub-header {
#             font-family: 'Arial', sans-serif;
#             color: #3B3B3B;
#             text-align: center;
#             font-size: 1.2rem;
#             margin-bottom: 2rem;
#         }
#         .nav-btn {
#             margin: 10px;
#             padding: 10px 15px;
#             font-size: 1rem;
#             border: none;
#             background: linear-gradient(90deg, #00c6ff, #0072ff);
#             color: white;
#             border-radius: 25px;
#             cursor: pointer;
#             transition: 0.3s;
#         }
#         .nav-btn:hover {
#             background: linear-gradient(90deg, #0072ff, #00c6ff);
#             box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Page content
# def main():
#     # Apply custom styles
#     apply_custom_styles()

#     # Header section
#     st.markdown("<h1 class='main-header'>Welcome to Your Project Landing Page</h1>", unsafe_allow_html=True)
#     st.markdown(
#         "<p class='sub-header'>Streamlined insights into sentiment analysis for Amazon and Flipkart reviews." \
#         " Gain actionable insights with cutting-edge technology!</p>",
#         unsafe_allow_html=True
#     )

#     # Add an image
#     img_path = "./assets/img00.jpg"  # Your preferred image path
#     try:
#         image = Image.open(img_path)
#         st.image(image, use_column_width=True)
#     except FileNotFoundError:
#         st.warning("Image not found. Please check the path.")

#     # Navigation buttons
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         if st.button("Explore Events", key="events_btn"):
#             switch_page("events")

#     with col2:
#         if st.button("Manage Attendees", key="attendees_btn"):
#             switch_page("attendees")

#     with col3:
#         if st.button("Track Tasks", key="tasks_btn"):
#             switch_page("tasks")

#     # Footer
#     st.markdown(
#         "<p style='text-align:center;margin-top:2rem;font-size:0.9rem;color:#7D7D7D;'>"
#         "Built with <span style='color:#E74C3C;'>♥</span> using Streamlit and Flask</p>",
#         unsafe_allow_html=True
#     )

# if __name__ == "__main__":
#     main()
#---------------------------------------------------------------

import streamlit as st

# Title of the landing page with a fancy style
st.markdown("""
# 🎉 **Event Management System**
Welcome to your one-stop solution for managing events, attendees, and tasks with ease. 

Designed to streamline the process of organizing events and keeping track of important tasks. 🚀
""", unsafe_allow_html=True)

# Introduction Section with Emojis
st.subheader("🌟 About the Project")
st.markdown("""
This **Event Management System** helps event organizers create events, manage attendees, and assign tasks. It features a user-friendly interface and robust backend to keep everything running smoothly. 

Key highlights:
- Manage events 🗓️
- Add and track attendees 👥
- Assign and monitor tasks ✅
- Real-time progress tracking 📊
- Data is stored securely in **SQLite** 🔒
""", unsafe_allow_html=True)

# Features Section with Fancy Styling
st.subheader("✨ Key Features")
st.markdown("""
- **📝 Event Creation**: Effortlessly create and manage events with detailed information.
- **👤 Attendee Management**: Add attendees, keep track of their participation, and view their status.
- **🔧 Task Assignment**: Assign tasks to attendees with deadlines and monitor their completion.
- **📈 Status Tracking**: Check the status of tasks and make sure everything is on track for your event.
- **📡 SQLite Integration**: Reliable and scalable database to store all your data.
""", unsafe_allow_html=True)

# Call to Action with Step-by-Step Guide
st.subheader("🛠️ How to Use the App")
st.markdown("""
1. **Create an Event**: Start by adding event details like name, description, and date.
2. **Add Attendees**: Invite attendees and assign them to your event.
3. **Assign Tasks**: Allocate tasks with clear deadlines to each attendee.
4. **Track Progress**: Monitor how tasks are progressing and ensure everything is on track for the event.
""", unsafe_allow_html=True)

# Contact Form Section with Styling
st.subheader("📬 Contact Us")
st.markdown("Have any questions or suggestions? We'd love to hear from you! 😃")

with st.form(key='contact_form'):
    name = st.text_input("Your Name ✍️")
    email = st.text_input("Your Email 📧")
    message = st.text_area("Your Message 💬")
    submit_button = st.form_submit_button(label="Send Message ✨")

if submit_button:
    st.write(f"Thank you for contacting us, {name}! We'll get back to you soon. 😊")

# Footer Section with Stylish Design
st.markdown("""
---
Made with ❤️ by [Kavacin](https://github.com/Kavacin) 🎨
""", unsafe_allow_html=True)
