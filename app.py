import streamlit as st
import os
from dotenv import load_dotenv

from pages.service_overview import overview_txt
from pages.irish_data_chatbot import irish_data_chatbot
from subs.styles import get_no_sidebar_style

load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


st.set_page_config(
    page_title="Emerald Insights",
    page_icon="🏭",
)
st.image("./images/header.png")
st.markdown("Created by Saeed Misaghian")
st.title("The Irish Power Data Chatbot 💬")

st.markdown("📧 Contact me: [sa.misaghian@gmail.com](mailto:sam.misaqian@gmail.com)")
st.markdown("🔗 [GitHub](https://github.com/SaM-92)")
st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)")


def page0():
    overview_txt()


# def page2():
#     st.markdown("""trend analysis""")


# Define your pages
def page1():
    irish_data_chatbot()


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:", ("✨Service Overview✨", "🇮🇪Irish Data Chatbot☘️")
)

if page == "🇮🇪Irish Data Chatbot☘️":
    page1()
# elif page == "Trend Analysis":
#     page2()
elif page == "✨Service Overview✨":
    page0()

# Apply the no sidebar style
no_sidebar_style = get_no_sidebar_style()
st.markdown(no_sidebar_style, unsafe_allow_html=True)
