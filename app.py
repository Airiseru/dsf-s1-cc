import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import calendar

# Constants
COLOR_RED = "#ce3c1b"
COLOR_YELLOW = "#f5ba01"
COLOR_LIGHTGREEN = "#9acba2"
COLOR_GREEN = "#41916c"
COLOR_BLUE = "#213875"
COLORS = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_LIGHTGREEN]
PROJ_TITLE = "An Analysis on AAC's Customers and their Spending Behaviors"
FIG_SIZE = (10, 5)

# Loading the datasets
unique_holders = pd.read_csv('data/s1_users_csv.csv')
df_with_label = pd.read_csv('data/s1_final_csv.csv')

# Dividing the categories into physical, digital, or others
physical_cats = ['grocery_pos', 'gas_transport', 'shopping_pos', 'misc_pos']
digital_cats = ['grocery_net', 'shopping_net', 'misc_net']
other_cats = [cat for cat in df_with_label['category'].unique() if cat not in physical_cats and cat not in digital_cats]

# Functions
def get_category_type(cat):
    if cat in physical_cats:
        return "Physical"
    elif cat in digital_cats:
        return "Digital"
    else:
        return "Others"

def phys_digi_avg_spending_per_gen(df, unique_key):
    avg_per_gen_type = pd.pivot_table(df, values='amt', index='category_type', columns='generation')

    # Turn the values into whole numbers
    for cat in avg_per_gen_type.columns:
        avg_per_gen_type[cat] = avg_per_gen_type[cat].apply(lambda x: np.round(x))
    
    # Add the bar charts
    fig = go.Figure(
        go.Bar(name='Silent Generation', x=avg_per_gen_type.index, y=avg_per_gen_type['Silent Generation'], marker_color=COLORS[0])
    )

    fig.add_trace(
        go.Bar(name='Baby Boomers', x=avg_per_gen_type.index, y=avg_per_gen_type['Baby Boomers'], marker_color=COLORS[1])
    )

    fig.add_trace(
        go.Bar(name='Generation X', x=avg_per_gen_type.index, y=avg_per_gen_type['Generation X'], marker_color=COLORS[2])
    )

    fig.update_layout(barmode='group')
    st.plotly_chart(fig, key=unique_key)


def cat_lvl_avg_spending_per_gen(df, unique_key):
    avg_per_gen_cat = pd.pivot_table(df, values='amt', index='category', columns='generation')

    # Turn the values into whole numbers
    for cat in avg_per_gen_cat.columns:
        avg_per_gen_cat[cat] = avg_per_gen_cat[cat].apply(lambda x: np.round(x))

    # Rename the index (category names)
    avg_per_gen_cat.index = ['Entertainment', 'Food and Dining', 'Gas Transport', 'Online Grocery', 'Physical Grocery',
                         'Health and Fitness', 'Home', 'Kids and Pets', 'Online Miscellaneous', 'Physical Miscellaneous',
                         'No Category', 'Personal Care', 'Online Shopping', 'Physical Shopping', 'Travel']

    # Add the graphs
    fig = go.Figure(
        go.Bar(name='Silent Generation', x=avg_per_gen_cat['Silent Generation'], y=avg_per_gen_cat  .index, marker_color=COLORS[0], orientation='h')
    )

    fig.add_trace(
        go.Bar(name='Baby Boomers', x=avg_per_gen_cat['Baby Boomers'], y=avg_per_gen_cat.index, marker_color=COLORS[1], orientation='h')
    )

    fig.add_trace(
        go.Bar(name='Generation X', x=avg_per_gen_cat['Generation X'], y=avg_per_gen_cat.index, marker_color=COLORS[2], orientation='h')
    )
    
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, key=unique_key)

def plot_avg_monthly_spending(df, unique_key):
    # Filter by Physical or Digital Category
    physical_trans = df[df['category_type'] == "Physical"].sort_values(by='trans_datetime')
    physical_trans = physical_trans[['trans_year', 'trans_month', 'amt']] # get specific columns
    digital_trans = df[df['category_type'] == "Digital"].sort_values(by='trans_datetime')
    digital_trans = digital_trans[['trans_year', 'trans_month', 'amt']]

    # Filter to transactions made in 2020
    physical_2020 = physical_trans[physical_trans['trans_year'] == 2020]
    physical_2020 = physical_2020[['trans_month', 'amt']]
    digital_2020 = digital_trans[digital_trans['trans_year'] == 2020]
    digital_2020 = digital_2020[['trans_month', 'amt']]

    # Filter to transactions made in 2021
    physical_2021 = physical_trans[physical_trans['trans_year'] == 2021]
    physical_2021 = physical_2021[['trans_month', 'amt']]
    digital_2021 = digital_trans[digital_trans['trans_year'] == 2021]
    digital_2021 = digital_2021[['trans_month', 'amt']]

    # Get the average transactions made in 2020
    phys_trans_data = physical_2020.groupby('trans_month')['amt'].mean().to_frame(name='avg').reset_index() # group the transactions by month and get the avg
    phys_trans_data['month'] = phys_trans_data['trans_month'].apply(lambda x: calendar.month_name[x]) # get the month name
    phys_trans_data['date'] = pd.to_datetime(("2020 " + phys_trans_data['month']), dayfirst=True) # convert the date into year, month
    phys_trans_data.drop(columns=['trans_month', 'month'], axis=1, inplace=True) # drop the other columns

    dig_trans_data = digital_2020.groupby('trans_month')['amt'].mean().to_frame(name='avg').reset_index() # group the transactions by month and get the avg
    dig_trans_data['month'] = dig_trans_data['trans_month'].apply(lambda x: calendar.month_name[x]) # get the month name
    dig_trans_data['date'] = pd.to_datetime(("2020 " + dig_trans_data['month']), dayfirst=True) # convert the date into year, month
    dig_trans_data.drop(columns=['trans_month', 'month'], axis=1, inplace=True) # drop the other columns

    # Get the average transactions made in 2021
    phys_trans_data2 = physical_2021.groupby('trans_month')['amt'].mean().to_frame(name='avg').reset_index() # group the transactions by month and get the avg
    phys_trans_data2['month'] = phys_trans_data2['trans_month'].apply(lambda x: calendar.month_name[x]) # get the month name
    phys_trans_data2['date'] = pd.to_datetime(("2021 " + phys_trans_data2['month']), dayfirst=True) # convert the date into year, month
    phys_trans_data2.drop(columns=['trans_month', 'month'], axis=1, inplace=True) # drop the other columns

    dig_trans_data2 = digital_2021.groupby('trans_month')['amt'].mean().to_frame(name='avg').reset_index() # group the transactions by month and get the avg
    dig_trans_data2['month'] = dig_trans_data2['trans_month'].apply(lambda x: calendar.month_name[x]) # get the month name
    dig_trans_data2['date'] = pd.to_datetime(("2021 " + dig_trans_data2['month']), dayfirst=True) # convert the date into year, month
    dig_trans_data2.drop(columns=['trans_month', 'month'], axis=1, inplace=True) # drop the other columns

    # Combine and round the average number
    phys_trans_data = pd.concat([phys_trans_data, phys_trans_data2], ignore_index=True) # combine the avg transactions made in 2020 and 2021
    phys_trans_data['avg'] = phys_trans_data['avg'].apply(lambda x: round(x)) # round avg value
    phys_trans_data = phys_trans_data.rename(columns={"avg": "Physical"}) # rename column
    dig_trans_data = pd.concat([dig_trans_data, dig_trans_data2], ignore_index=True) # combine the avg transactions made in 2020 and 2021
    dig_trans_data['avg'] = dig_trans_data['avg'].apply(lambda x: round(x)) # round avg value
    dig_trans_data = dig_trans_data.rename(columns={"avg": "Digital"}) # rename column

    # Combine into one dataframe
    avg_trans = phys_trans_data.merge(dig_trans_data, on='date', how='inner')

    # Plot
    fig = px.line(avg_trans, x='date', y=['Physical', 'Digital'],
                color_discrete_sequence=COLORS,
                labels= {"variable": "Category Type"}
                )

    fig.update_layout(xaxis_title="", yaxis_title="",
                    plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, key=unique_key)

# HTML Styles
html_styles = f"""
<style>
    h3 {{
        color: {COLOR_RED};
    }}

    h4 {{
        padding-bottom: 0;
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

# Update df_with_label
df_with_label['category_type'] = df_with_label['category'].map(get_category_type)

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
    st.markdown("To learn more about the dataset, this page will showcase the data preprocessing done, do some initial exploration of the data through graphs and charts, and showcase how the clustering was done using KMeans. To view the whole code, you can check the [Jupyter Notebook](https://github.com/Airiseru/dsf-s1-cc/blob/main/cc-project-nb.ipynb) for more.")
    st.write("<br>", unsafe_allow_html=True)

    with st.expander("⚙️ **Data Preprocessing**", expanded=True):
        initial_df = pd.read_csv('cc_dirty.csv')

        st.markdown("Shown below is the first 10 rows of the initial dataset:")
        st.dataframe(initial_df.head(10))
        st.markdown("To prepreprocess the data, the following steps were done:\n1. Drop duplicate rows and rows with null values in the `job` column. For the `category` column, `null` values were replaced with `no_category`\n2. Standardized the `gender` column to only contain `F` or `M`\n3. Removed the dollar ($) sign in the `amt` column and converted it to a `float` datatype\n4. Remove the word 'people' and the comma from the `city_pop` column and then converted it to an integer type\n5. Converted the `dob` and `unix_time` columns to a datetime format\n6. Added columns such as `age`, `generation` of the customer, the hour/month/year of the transaction, and the number of days that has passed since the date of transaction to January 1, 2022 (`elapsed_days`)")
        st.markdown("\nThus from the initial 100,000 transactions, it was down to 92,432 transactions after cleaning.")
    
    with st.expander("🔍 **Exploratory Data Analysis**", expanded=True):
        st.write("To do an initial exploration of the data, the following were examined:\n1. Timeline of transaction\n2. Number of account holders (customers)\n3. Gender distribution\n4. Age distribution (based on generation)\n5. City distribution\n6. Categories with the highest number of transactions\n7. Categories with the highest amount spent")

        # Transaction Timeline and Number of Account Holders
        st.markdown("<h4>Transaction Timeline and Number of Account Holders</h4><br>", unsafe_allow_html=True)
        basic_info = {"Transaction Timeline": "January 1, 2020 - December 6, 2021",
                      "Number of Account Holders": 94}
        basic_info_df = pd.DataFrame.from_dict(basic_info, orient='index', columns=["Info"])
        st.table(basic_info_df)

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
        st.write("To cluster the customers into groups, the K-Means algorithm was used. The customers were clustered to further examine the different groups of customers the company had and their specific behaviors. They were grouped based on their recency, frequency, and monetary values.")

        st.markdown("**Definitions**")
        st.markdown("1. Recency - how many days ago (from January 1, 2022) was the most recent transaction made by the customer?\n2. Frequency - how often does the customer use their credit card (or in total, how many transactions did he/she make)?\n3. Monetary - in total, how much money did the customer spend?")

        st.markdown("**Steps**")
        st.markdown("1. Scale the values: this was done since the values (especially the monetary) had a wide range of values, which may negatively impact the model.\n2. Running the K-Means algorithm at different number of cluster values (from 2 to 10 clusters)\n3. Selecting the most optimal number of clusters: for this, we used 6 clusters for a more focused exploration of the customers")

        st.markdown("*To see the whole code for generating the clusters, check out the [Jupyter Notebook](https://github.com/Airiseru/dsf-s1-cc/blob/main/cc-project-nb.ipynb)!*")

elif my_page == 'Results':
    st.write('___')
    st.write("After doing K Means clustering, 6 clusters or groups of customers were formed. The table below summarizes the different groups and their average RFM values.")
    st.markdown(
        f"""| Cluster | Recency Value | Frequency Value | Monetary Value |
| ------- | ------------- | --------------- | -------------- |
| 0       | Low (316)     | Low (8)         | Low (5,382)    |
| 1       | High (25)     | High (1,309)    | High (91,383)  |
| 2       | Medium (124)  | Low (11)        | Low (5,136)    |
| 3       | High (25)     | Very High (1,957)| Very High (133,899) |
| 4       | Low (604)     | Low (8)         | Low (4,434)    |
| 5       | High (25)     | Medium (656)    | Medium (45,917)|"""
    )
    st.write("From this, we can observe that clusters 0 and 4 had little to no interaction with the company compared to the other groups. They will be ignored for now as these customers may require more resources to encourage them to use their cards more, which might be unprofitable for the company. As such, no analysis or business recommendations will be done for these clusters for now.")

    st.write("Instead, it is encouraged to focus on increasing the engagement of the consistent customers as they are more beneficial to the company and a greater return on investment.")

    st.subheader("Deep Dive Analysis of the Clusters")
    st.write("For each cluster, we will be examining their behaviors. Specifically, we will look at how many transactions and users are in the cluster, the age range of the customers, and their average spending per month and per category.")

    # Dropdown for cluster 1
    with st.expander("🛒 **Cyber Savvy Shoppers** *(cluster 1)*", expanded=False):
        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        c1_trans = df_with_label[df_with_label['labels'] == 1]
        c1_users = unique_holders[unique_holders['labels'] == 1]
        phys_digi_avg_spending_per_gen(c1_trans, "cluster1-digi-vs-phys")

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c1_trans, "cluster1-category-avg")

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c1_trans, "cluster1-avg-spending")
    
    # Dropdown for cluster 2
    with st.expander("🛒 **Epic Comeback Connoisseurs** *(cluster 2)*", expanded=False):
        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        c2_trans = df_with_label[df_with_label['labels'] == 2]
        c2_users = unique_holders[unique_holders['labels'] == 2]
        phys_digi_avg_spending_per_gen(c2_trans, "cluster2-digi-vs-phys")

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c2_trans, "cluster2-category-avg")

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c2_trans, "cluster2-avg-spending")

    # Dropdown for cluster 3
    with st.expander("🛒 **Digital Dynamos** *(cluster 3)*", expanded=False):
        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        c3_trans = df_with_label[df_with_label['labels'] == 3]
        c3_users = unique_holders[unique_holders['labels'] == 3]
        phys_digi_avg_spending_per_gen(c3_trans, "cluster3-digi-vs-phys")

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c3_trans, "cluster3-category-avg")

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c3_trans, "cluster3-avg-spending")
    
    # Dropdown for cluster 5
    with st.expander("🛒 **Festive Spenders** *(cluster 5)*", expanded=False):
        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        c5_trans = df_with_label[df_with_label['labels'] == 5]
        c5_users = unique_holders[unique_holders['labels'] == 5]
        phys_digi_avg_spending_per_gen(c5_trans, "cluster5-digi-vs-phys")

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c5_trans, "cluster5-category-avg")

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c5_trans, "cluster5-avg-spending")
    
    st.subheader("Summary of Findings and Recommendations")

elif my_page == "Summary":
    st.write('___')