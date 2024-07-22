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
COLORS = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_LIGHTGREEN]
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
    st.markdown("To learn more about the dataset, this page will showcase the data preprocessing done, explore the data through graphs and charts, and showcase how the clustering was done using KMeans. To view the whole code, you can check the [Jupyter Notebook](https://github.com/Airiseru/dsf-s1-cc/blob/main/cc-project-nb.ipynb) for more.")
    st.write("<br>", unsafe_allow_html=True)

    with st.expander("⚙️ **Data Preprocessing**", expanded=True):
        initial_df = pd.read_csv('cc_dirty.csv')

        st.markdown("Shown below is the first 10 rows of the initial dataset:")
        st.dataframe(initial_df.head(10))
        st.markdown("To prepreprocess the data, the following steps were done:\n1. Drop duplicate rows and rows with null values\n2. Standardized the `gender` column to only contain `F` or `M`\n3. Removed the dollar ($) sign in the `amt` column and converted it to a `float` datatype\n4. Remove the word 'people' and the comma from the `city_pop` column and then converted it to an integer type\n5. Converted the `dob` and `unix_time` columns to a datetime format\n6. Added columns such as `age`, `generation` of the customer, the hour/month/year of the transaction, and the number of days that has passed since the date of transaction to January 1, 2022 (`elapsed_days`)")
        st.markdown("\nThus from the initial 100,000 transactions, it was down to 92,432 transactions after cleaning.")
    
    with st.expander("🔍 **Exploratory Data Analysis**", expanded=True):
        st.write("To do an initial exploration of the data, the following were looked at:\n1. Timeline of transaction\n2. Number of account holders (customers)\n3. Gender distribution\n4. Age distribution (based on generation)\n5. City distribution\n6. Categories with the highest number of transactions\n7. Categories with the highest amount spent")
        st.markdown("<h4>Transaction Timeline and Number of Account Holders</h4>", unsafe_allow_html=True)
        # insert the timeline and number of account holders

        # Gender Distribution Plot
        st.markdown("<h4>Gender Distribution</h4>", unsafe_allow_html=True)
        gender_count = unique_holders['gender'].value_counts().to_frame(name="count").reset_index()
        gender_fig = px.bar(gender_count, x='gender', y='count', color='gender')
        st.plotly_chart(gender_fig, key='gender_distri_plot')
        st.write("This plot tells us that the majority of the customers of AAC are male, which consists of 93% of the customers.")

        # Age Distribution per Generation plot
        st.markdown("<h4>Age Distribution</h4>", unsafe_allow_html=True)
        generation_count = unique_holders['generation'].value_counts().to_frame(name="count").reset_index()
        generation_count = generation_count[generation_count['count'] > 0]
        generation_fig = px.bar(generation_count, x='generation', y='count', color='generation')
        st.plotly_chart(generation_fig, key='generation_distri_plot')
        st.write("Around 58% of the customers are Baby Boomers, which has the age range of 58 to 76. The youngest customer is 51 years old while the eldest is at 95 years old. The customer base of AAC has an average age of 67 years old.")

        # City Distribution
        st.markdown("<h4>City Distribution</h4>", unsafe_allow_html=True)
        top_city_count = unique_holders['city'].value_counts()[0:5].to_frame(name="count").reset_index()
        top_city_fig = px.bar(top_city_count, x='city', y='count', color='city')
        st.plotly_chart(top_city_fig, key='top_city_distri_plot')
        st.write("Out of the 94 unique customers, 5 live in San Fernando, 4 in Dasmarinas and Calapan, and 3 in Masbate and Pagadian. The rest live in other cities but the top city is San Fernando.")

        # Categories based on number of transactions plot
        st.markdown("<h4>Category based on number of transactions</h4>", unsafe_allow_html=True)
        category_names = {"grocery_pos": "Physical Grocery",
                  "shopping_pos": "Physical Shopping",
                  "gas_transport": "Gas and Transportation",
                  "kids_pets": "Kids and Pets",
                  "home": "Home",
                  "no_category": "No Category",
                  "personal_care": "Personal Care",
                  "food_dining": "Food and Dining",
                  "entertainment": "Entertainment",
                  "misc_pos": "Physical Miscellaneous",
                  "health_fitness": "Health and Fitness",
                  "shopping_net": "Online Shopping",
                  "travel": "Travel",
                  "misc_net": "Online Miscellaneous",
                  "grocery_net": "Online Grocery"}
        cat_trans = df_with_label.groupby(['category'])['trans_datetime'].count().sort_values(ascending=False).to_frame("count").reset_index()
        cat_trans['category'] = cat_trans['category'].map(category_names)

        cat_trans_fig = px.bar(cat_trans, x='count', y='category', color='category',
                    labels={"count": "Number of Transactions"})
        cat_trans_fig.update_layout(showlegend=False)
        st.plotly_chart(cat_trans_fig, key='category_per_trans_fig')
        st.write("We observe that the category that has the most number of transactions would be Physical Grocery. That is, grocery done face-to-face or physically.")

        # Categories based on amount spent
        st.markdown("<h4>Category based on the amount spent</h4>", unsafe_allow_html=True)
        cat_sum = df_with_label.groupby('category')['amt'].sum().sort_values(ascending=False).to_frame("total").reset_index()
        cat_sum['category'] = cat_sum['category'].map(category_names)

        cat_sum_fig = px.bar(cat_sum, x='total', y='category', color='category',
                    labels={"total": "Total Amount Spent"})
        cat_sum_fig.update_layout(showlegend=False)
        st.plotly_chart(cat_sum_fig, key='category_per_amt_fig')
        st.write("Similarly, the Physical Grocery category has the highest amount spent. This may due to the number of transactions as notably, the more transactions on the category, the more amount is spent.")

        # Summary of EDA
        st.markdown("<h4>Summary of Findings</h4>", unsafe_allow_html=True)
        st.write("Based on the plots, we can notice a few things.")
        st.markdown(f"1. All of the customers of AAC are more on the older generation (50 and above).\n2. Majority of the customers are located in the Luzon area.\n3. Based on the overall transaction history, the customers tend to buy products physically or face-to-face.\n4. The top category in terms of number of transactions and amount spent is `Physical Grocery`. This may indicate that the customers tend to use their cards to buy grocery physically.")

    with st.expander("👥 **Clustering**", expanded=True):
        st.write("wow!")
    # Create a dropdown for 1) Data Preprocessing 2) EDA 3) Method for Clustering

elif my_page == 'Results':
    st.write('___')
    # Create a dropdown for each cluster

elif my_page == "Summary":
    st.write('___')