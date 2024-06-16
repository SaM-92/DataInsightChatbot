import streamlit as st


def overview_txt():
    st.markdown(
        """
    🔌 About the CleanEnergyBot

    Initially started as a Telegram bot, CleanEnergyBot has been providing users with key information on clean energy.
    """
    )
    st.image("./images/CleanEnergyBot_icon.png", width=250)
    st.markdown(
        """
    🚀 What’s New?

    We’re taking a leap forward to offer detailed insights to interested users, energy consultants, and data scientists keen on exploring the power system data of Ireland.
    
    💡 Current Service Overview

    🤖 1. Chat with Data

    🎙 Ask anything: Pose any query from 2014 to 2024 regarding the Irish power system, and let the bot assist you with answers and visual plots.
    
    🧘 Be patient: As a new service in its initial test phase, and provided for free, we appreciate your patience and understanding.
      """
    )

    hidden_text = """
    📊 2. Trend Analysis

    🕵️‍♂️ Deep Dive: Gain comprehensive insights into the Irish power system. Specify intervals, select times, years, and parameters like wind or demand, and choose your plot type—all with just a few clicks.

    🌟 3. Upcoming Updates

    Stay tuned for exciting new features and enhancements to make your data analysis journey even more insightful and convenient.
    """
