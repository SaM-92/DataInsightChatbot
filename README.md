# Emerald Insights: SQL Query and Data Analysis Chatbot 💬

## Technologies Used

![LangChain](https://img.shields.io/badge/LangChain-%2300A9C0.svg?style=for-the-badge&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-%2300A9C0.svg?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%234169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-%2307406E.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%230E4A7E.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)

## Overview

![Real-time Data Scraping Diagram](/images/overview.gif)

Emerald Insights is a chatbot application providing insights and visualizations about the Irish power system from 2014 to 2024. It uses Streamlit for the front-end and integrates advanced backend technologies such as LangChain, OpenAI, SQL, and Python agents for data processing and retrieval.

## Key Technologies and Techniques:

- LangChain: Orchestrates the chatbot workflow, integrating SQL and Python agents for seamless data interaction and processing.

- OpenAI: Utilizes the GPT-4 model for natural language understanding and response generation, enabling the chatbot to interpret and respond to user queries accurately.

- SQL and Python Agents:

  - SQL Agents: Generate and execute SQL queries against the system database for precise data retrieval.
  - Python Agents: Execute Python scripts to process data and create visualizations using matplotlib.

- Prompt Engineering:

  - Few-Shot Prompt Templates: Guide the language model in generating accurate SQL queries and responses.
  - System Message Templates: Define detailed instructions for handling various query types.

- Semantic Similarity Example Selector: Matches user queries with relevant examples to improve response accuracy.

## Example Code Insights:

- Database Connection: Connects to an SQLite database containing system data using the SQLDatabase utility.
- Sequential Chains: Combines SQL query execution and Python data processing for end-to-end data retrieval and visualization.
- Post-Processing: Formats responses from the language model for presentation in the Streamlit interface.

## Setup

### Prerequisites

- See `requirements.txt` file

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SaM-92/emerald-insights.git
   cd emerald-insights
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root directory.
   - Add your OpenAI API Key to the `.env` file:
     ```bash
     OPENAI_API_KEY=your_openai_api_key_here
     ```

### Running the Application

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL to interact with the chatbot.

## Project Structure

```plaintext
emerald-insights/
├── images/
│   └── header.png
├── pages/
│   ├── service_overview.py
│   └── irish_data_chatbot.py
├── subs/
│   ├── __init__.py
│   ├── agent.py
│   ├── db_connections.py
│   ├── prompts.py
│   ├── styles.py
│   └── visualisation.py
├── data/
│   └── eirgrid_data.db
├── .env
├── app.py
├── requirements.txt
└── README.md
```

## Key Components

- `app.py`
  This is the main entry point of the application. It sets up the page configurations, navigation, and loads the respective pages based on user interaction.

- `pages/service_overview.py`
  Contains the overview of the service which is displayed on the "Service Overview" page.

- `pages/irish_data_chatbot.py`
  Contains the chatbot functionality to handle user queries about the Irish power system.

- `subs/`
  This directory contains various modules to support the application: - `agent.py`: Handles AI agents. - `db_connections.py`: Handles database connections. - `prompts.py`: Contains the templates and logic for generating prompts. - `styles.py`: Provides styles for the Streamlit application. - `visualisations.py`: Functions to visualize data in response to user queries.

### Data

The data is hosted on a PostgreSQL database. Ensure your PostgreSQL instance is running and accessible.

## Contact

Created by Saeed Misaghian

- 📧 Email: [sa.misaghian@gmail.com](mailto:sa.misaghian@gmail.com)
- 🔗 [GitHub](https://github.com/SaM-92)
- 🔗 [LinkedIn](https://www.linkedin.com/in/saeed-misaghian/)
