import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Constants
COLOR_RED = "#ce3c1b"
COLOR_YELLOW = "#f5ba01"
COLOR_LIGHTGREEN = "#9acba2"
COLOR_GREEN = "#41916c"
COLOR_BLUE = "#213875"
PROJ_TITLE = "An Analysis on AAC's Customers and their Spending Behaviors"

# Loading the datasets
unique_holders = pd.read_csv('data/s1_users_csv.csv')
df_with_label = pd.read_csv('data/s1_final_csv.csv')

# Functions

# HTML Styles
html_styles = f"""
<style>
    h3 {{
        color: {COLOR_RED};
    }}

    p {{
        font-size: 1.125rem;
        text-align: justify;
    }}

    .card-design-red {{
        padding: 15px 30px;
        box-shadow: -8px -7px {COLOR_RED};
        border: 1px solid grey;
        border-radius: 20px;
        margin-top: 10px;
    }}

    .italicized {{
        font-style: italic;
    }}

    .capitalized {{
        text-transform: uppercase;
    }}

    .tabbed {{
        margin-left: 1.75rem;
        margin-top: 0;
    }}
</style>
"""

home_html = f"""
<style>
    .cards-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 2.5rem;
        text-align: center;
    }}

    .card {{
        flex: 15%;
    }}

    .card p {{
        text-align: center;
        padding: 0 1.5rem;
    }}

    .bullet-title {{
        margin-bottom: 0;
    }}

    .st-emotion-cache-eqffof li {{
        font-size: 1.1rem;
    }}
</style>
<h3>About the Project</h3>
<p>This project is about analyzing the company Adobo Advantage Cards (AAC). The main objective of this project is to gather information about AAC's customers based on their transaction history and suggest actionable steps the business can take to maintain or improve their customer's spending behaviors.</p>

<h3>Goals and Objectives</h3>
<p class='italicized'>How do we better drive the business?</p>
<div class='cards-container'>
    <div class='card card-design-red'>
        <h4>Customer Demographics</h4>
        <p>Understand the customers of the company</p>
        <p class='italicized'>Who are they?</p>
    </div>
    <div class="card card-design-red">
        <h4>Spending Behaviors</h4>
        <p>Understand how the customers spend their money or use their credit card</p>
        <p class="italicized">What do they keep buying?</p>
    </div>
    <div class='card card-design-red'>
        <h4>Steps and Strategies</h4>
        <p>Recommend actionable items to drive business growth</p>
        <p class='italicized'>What can AAC do knowing all this informtion?</p>
    </div>
</div>

<br>

<h3>About the Dataset</h3>
<p class='italicized'>What kind of information do we have?</p>
<div>
    <p>Transaction History Period: <span class='capitalized'>Jan 01, 2020 - Dec 07, 2021</span></p>
    <p class='bullet-title'>The dataset includes</p>
    <ul>
        <li>Different columns related to one's transaction
            <ul>
                <li>cc_num, acct_num, dob, job, amt, category, etc.</li>
            </ul>
        </li>
        <li>The "category" column was divided into three parts: physical, digital, and others
            <ul>
                <li>Example categories: grocery_pos, kids_pets, gas_trans, shopping_net, etc.</li>
                <li>net = digital transactions; pos = physical transactions</li>
            </ul>
        </li>
    <ul>
</div>

<br>

<h3>Scopes and Limitations</h3>
<p class='italicized'>What are the assumptions made? What did we analyze and cover?</p>
<p>The scope of the analysis is limited to 2020 to 2021 since that is the period covered by the dataset. Furthermore, it was assumed that the COVID-19 pandemic did not occur during this transaction period since it was discovered that majority of the customers are part of the older generations.</p>
<p>To ensure consistency, the categories that did not specify whether it was physical or digital were considered as "others". This is to ensure that there is no ambuigity between the transactions. Listed below are the categories considered to be physical, digital, or others.</p>
<ul>
    <li>Physical: grocery_pos, gas_transport, shopping_pos, misc_pos</li>
    <li>Digital: grocery_net, shopping_net, misc_net</li>
    <li>Others: kids_pets, food_dining, home, health_fitness, travel</li>
</ul>
"""

data_preprocessing_html = f"""
<h3></h3>
"""

# Creating the streamlit app
st.set_page_config(layout='wide')
st.subheader("From Piggy Banks to Pin Codes")
st.title(PROJ_TITLE)
st.markdown(html_styles, unsafe_allow_html=True)

my_page = st.sidebar.radio('Page Navigation',
                           ['About the Project', 'Methodology',
                            'Results', 'Summary'])

if my_page == 'About the Project':
    st.write('___')
    st.markdown(home_html, unsafe_allow_html=True)

elif my_page == "Methodology":
    st.write('___')
    st.subheader("Methodology")
    st.write("To learn more about")
    st.write("<br>", unsafe_allow_html=True)
    with st.expander("⚙️ **Data Preprocessing**", expanded=True):
        st.write("wow!")
    
    with st.expander("🔍 **Exploratory Data Analysis**", expanded=True):
        st.write("wow!")

    with st.expander("👥 **Clustering**", expanded=True):
        st.write("wow!")
    # Create a dropdown for 1) Data Preprocessing 2) EDA 3) Method for Clustering

elif my_page == 'Results':
    st.write('___')
    # Create a dropdown for each cluster

elif my_page == "Summary":
    st.write('___')