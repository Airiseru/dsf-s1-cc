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

def phys_digi_avg_spending_per_gen(df, unique_key, greatest_gen=False):
    avg_per_gen_type = pd.pivot_table(df, values='amt', index='category_type', columns='generation')

    # Turn the values into whole numbers
    for cat in avg_per_gen_type.columns:
        avg_per_gen_type[cat] = avg_per_gen_type[cat].apply(lambda x: np.round(x))
    
    # Add the bar charts
    fig = go.Figure(
        go.Bar(name='Silent Generation', x=avg_per_gen_type.index, y=avg_per_gen_type['Silent Generation'], marker_color=COLORS[0])
    )

    fig.add_trace(
        go.Bar(name='Baby Boomers', x=avg_per_gen_type.index, y=avg_per_gen_type['Baby Boomers'], marker_color=COLORS[2])
    )

    fig.add_trace(
        go.Bar(name='Generation X', x=avg_per_gen_type.index, y=avg_per_gen_type['Generation X'], marker_color=COLORS[1])
    )

    if greatest_gen:
        fig.add_trace(
            go.Bar(name='Greatest Generation', x=avg_per_gen_type.index, y=avg_per_gen_type['Greatest Generation'], marker_color="black")
        )

    fig.update_layout(barmode='group')
    st.plotly_chart(fig, key=unique_key)


def cat_lvl_avg_spending_per_gen(df, unique_key, greatest_gen=False):
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
        go.Bar(name='Baby Boomers', x=avg_per_gen_cat['Baby Boomers'], y=avg_per_gen_cat.index, marker_color=COLORS[2], orientation='h')
    )

    fig.add_trace(
        go.Bar(name='Generation X', x=avg_per_gen_cat['Generation X'], y=avg_per_gen_cat.index, marker_color=COLORS[1], orientation='h')
    )

    if greatest_gen:
       fig.add_trace(
            go.Bar(name='Greatest Generation', x=avg_per_gen_cat['Greatest Generation'], y=avg_per_gen_cat.index, marker_color='black', orientation='h')
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
        c1_trans = df_with_label[df_with_label['labels'] == 1]
        c1_users = unique_holders[unique_holders['labels'] == 1]

        st.markdown("<h4>General Information about the Customers in the Cluster</h4><br>", unsafe_allow_html=True)
        info_dict = {"Number of Transactions": len(c1_trans),
                    "Number of Users": len(c1_users),
                    "Minimum Age": c1_users['age'].min(),
                    "Mean Age": np.round(c1_users['age'].mean(), 2),
                    "Maximum Age": c1_users['age'].max()
                    }
        
        info_array = np.array(list(info_dict.items()))
        info_df = pd.DataFrame(info_array)
        info_df.columns = ["Info", "Value"]
        info_df.set_index("Info", inplace=True)
        st.table(info_df)

        generation_counts = c1_users['generation'].value_counts()
        generation_df = pd.DataFrame(generation_counts)

        st.markdown("<h4>Distribution of Customer per Generation</h4>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=generation_df.index, y=generation_df['count'], marker_color=COLORS[2::-1]))
        st.plotly_chart(fig, key="c1-cluster-info")

        st.write("Majority of the customers of this class are from the Baby Boomers generation. Note that this cluster had a high recency, high frquency, and high monetary value. Which means that this cluster is the cream of the crop of the company, they are the highest valued customers.")

        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        phys_digi_avg_spending_per_gen(c1_trans, "cluster1-digi-vs-phys")

        st.markdown("From this graph, we notice that across the generations, the average spending on digital categories is greater than any other categories. Interestingly enough, the **average spending of the Silent Generation in the digital category is equal to the average spending of the Baby Boomers** even though there is <u>significantly more Baby Boomers</u> in this cluster.", unsafe_allow_html=True)

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c1_trans, "cluster1-category-avg")

        st.markdown("In terms of specific categories across the generations, majority of the spendings are still on digital categories. Specifically for Baby Boomers and Generation X, they tend to spend more on Online Shopping while the Silent Generation tends to spend more on the Online Miscellaneous category.<br><br>This simply indicates that for this cluster, they tend to use their card and spend more through online methods rather than physical components. However, it doesn't mean that these generations don't spend their cards for physical categories. In fact, it can be seen that for all generations, they tend to spend more for categories such as Physical Grocery compared to its counterpart (Online Grocery).", unsafe_allow_html=True)

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c1_trans, "cluster1-avg-spending")

        st.markdown("Overall, the **average monthly spending on digital categories** across the the whole timeline of the transaction history is **greater than** then physical categories, especially in the month of October. This may indicate that this cluster tend to use their cards more in the month of October, which the company can capitalize on by <u>doing more promotions and offers for online products</u> in this month.<br><br>Furthermore, it can be seen that for the month of November and the start of December, this cluster tends to spend their cards more on physical transactions rather than digital. This may imply that **during the Christmas season, this cluster may tend to go out and use their cards as they physically meet people**, which can potentially be another marketing approach for the company. Specifically, the company can <u>offer discounts or special deals for the Christmas season</u>.", unsafe_allow_html=True)
    
    # Dropdown for cluster 2
    with st.expander("🛒 **Epic Comeback Connoisseurs** *(cluster 2)*", expanded=False):
        c2_trans = df_with_label[df_with_label['labels'] == 2]
        c2_users = unique_holders[unique_holders['labels'] == 2]

        st.markdown("<h4>General Information about the Customers in the Cluster</h4><br>", unsafe_allow_html=True)
        info_dict = {"Number of Transactions": len(c2_trans),
                    "Number of Users": len(c2_users),
                    "Minimum Age": c2_users['age'].min(),
                    "Mean Age": np.round(c2_users['age'].mean(), 2),
                    "Maximum Age": c2_users['age'].max()
                    }
        
        info_array = np.array(list(info_dict.items()))
        info_df = pd.DataFrame(info_array)
        info_df.columns = ["Info", "Value"]
        info_df.set_index("Info", inplace=True)
        st.table(info_df)

        generation_counts = c2_users['generation'].value_counts()
        generation_df = pd.DataFrame(generation_counts)

        st.markdown("<h4>Distribution of Customer per Generation</h4>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=generation_df.index, y=generation_df['count'], marker_color=COLORS[2::-1]))
        st.plotly_chart(fig, key="c2-cluster-info")

        st.markdown("Majority of the customers of this class are from the Baby Boomers generation as well. But the difference is that there are also customers who are part of the Greatest Generation, which are those who are of age 95 and above. Note that this cluster had a medium recency, low frquency, and low monetary value which means that this cluster **contains the customers who are slowly using their cards less**.")

        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        phys_digi_avg_spending_per_gen(c2_trans, "cluster2-digi-vs-phys", True)

        st.markdown("From this graph, we notice that across the generations, the **average spending on digital categories is greater than any other categories, except for Generation X**. For this generation, they tend to **spend more on the others categories**, with the digital category coming close. For the Greatest Generation, we see that they spend on Physical and Digital Categories almost equally.", unsafe_allow_html=True)

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c2_trans, "cluster2-category-avg", True)

        st.markdown("From further examination, we see that majority of the **average monthly spendings are indeed on online categories** such as Online Shopping and Online Miscellaneous. However, we can also see that these set of customers **spend little to no money on a lot of categories**, especially the **categories that may not be as essential** to them anymore such as travel, entertainment, etc. Also, for the **Greatest Generation, we see that they frequently spend a lot on both the Physical and Online Shopping**, which may suggest that this generation just loves to shop in general.", unsafe_allow_html=True)

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c2_trans, "cluster2-avg-spending")

        st.markdown("Overall, the **average monthly spending on digital categories** across the the whole timeline of the transaction history is **greater than** then physical categories. However, we notice a negative trend over the year, then a sudden spike, and slowly decline again. This may indicate that for certain periods, the cluster will **suddenly splurge and use their cards but as time passes, they will use their cards less**. This may be resisted by offering promotions or deals when the company notices a sudden decline of card usage for this cluster. The promotions should be done such that it encourages the cluster to use their card, especially through the categories they frequent in such as Online Shopping.", unsafe_allow_html=True)

    # Dropdown for cluster 3
    with st.expander("🛒 **Digital Dynamos** *(cluster 3)*", expanded=False):
        c3_trans = df_with_label[df_with_label['labels'] == 3]
        c3_users = unique_holders[unique_holders['labels'] == 3]

        st.markdown("<h4>General Information about the Customers in the Cluster</h4><br>", unsafe_allow_html=True)
        info_dict = {"Number of Transactions": len(c3_trans),
                    "Number of Users": len(c3_users),
                    "Minimum Age": c3_users['age'].min(),
                    "Mean Age": np.round(c3_users['age'].mean(), 2),
                    "Maximum Age": c3_users['age'].max()
                    }
        
        info_array = np.array(list(info_dict.items()))
        info_df = pd.DataFrame(info_array)
        info_df.columns = ["Info", "Value"]
        info_df.set_index("Info", inplace=True)
        st.table(info_df)

        generation_counts = c3_users['generation'].value_counts()
        generation_df = pd.DataFrame(generation_counts)

        st.markdown("<h4>Distribution of Customer per Generation</h4>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=generation_df.index, y=generation_df['count'], marker_color=COLORS[2::-1]))
        st.plotly_chart(fig, key="c3-cluster-info")

        st.markdown("Majority of the customers of this class are from the Baby Boomers generation with an equal amount of Generation X and Silent Generation. This cluster has a high recency, high frequency, and high monetary value, which is similar to the first cluster. The difference is that this cluster had a higher frquency and monetary value, **making them the most elite of the elite customers**.")

        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        phys_digi_avg_spending_per_gen(c3_trans, "cluster3-digi-vs-phys")

        st.markdown("From this graph, again, across the generations, we see that the **average spending on digital categories is greater than any other categories**. The difference from the first cluster is that the overall average spending for all types of categories are slightly greater.", unsafe_allow_html=True)

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c3_trans, "cluster3-category-avg")

        st.markdown("Looking into the average monthly spending per category, the graph shows that **all generations have a high average on Online Shopping and Travel**. Aside from Shopping, the average monthly spending between online categories and physical categories are close, which indicates that for this cluster, **they tend to use their card either way** (online or physical).", unsafe_allow_html=True)

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c3_trans, "cluster3-avg-spending")

        st.markdown("Overall, the **average monthly spending on digital categories** across the the whole timeline of the transaction history is **greater than** then physical categories. We also notice a lot of dips and sudden spikes on the monthly spending in digital transactions. This may indicate that this cluster may prefer **online means depending on the season or possible deals and offers available in the online medium**. But, we also see that for both years, **there is a spike in the month of April**, which the company can capitalize on. Further analysis on the transaction history could reveal more patterns between the spending behavior depending on the season or month.<br><br>Based on the graph, **there is also a constant average spending on physical categoreies**, which is another aspect the company can focus on. That is, instead of solely focusing on online deals and promotions, the company can continuously capitalize on the consistent physical spending to help maintain (or grow) the cluster's high monetary value.", unsafe_allow_html=True)
    
    # Dropdown for cluster 5
    with st.expander("🛒 **Festive Spenders** *(cluster 5)*", expanded=False):
        c5_trans = df_with_label[df_with_label['labels'] == 5]
        c5_users = unique_holders[unique_holders['labels'] == 5]

        st.markdown("<h4>General Information about the Customers in the Cluster</h4><br>", unsafe_allow_html=True)
        info_dict = {"Number of Transactions": len(c5_trans),
                    "Number of Users": len(c5_users),
                    "Minimum Age": c5_users['age'].min(),
                    "Mean Age": np.round(c5_users['age'].mean(), 2),
                    "Maximum Age": c5_users['age'].max()
                    }
        
        info_array = np.array(list(info_dict.items()))
        info_df = pd.DataFrame(info_array)
        info_df.columns = ["Info", "Value"]
        info_df.set_index("Info", inplace=True)
        st.table(info_df)

        generation_counts = c5_users['generation'].value_counts()
        generation_df = pd.DataFrame(generation_counts)

        st.markdown("<h4>Distribution of Customer per Generation</h4>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=generation_df.index, y=generation_df['count'], marker_color=COLORS[2::-1]))
        st.plotly_chart(fig, key="c5-cluster-info")

        st.markdown("Majority of the customers of this class are from the Baby Boomers generation with a decent amount from Generation X and Silent Generation and one user from the Greatest Generation. This cluster has a high recency, medium frequency, and medium monetary value, which makes this set of customers the typical customers of the company that **moderately uses their cards but more than the average customer**.")

        st.markdown("<h4>Physical vs Digital: Average Spending per Generation</h4>", unsafe_allow_html=True)
        phys_digi_avg_spending_per_gen(c5_trans, "cluster5-digi-vs-phys", True)

        st.markdown("From this graph, again, across the generations, we see that the **average spending on digital categories is greater than any other categories**. Also, we notice that across the different types of catergories, the **average spending of the customer in the Greatest Generation is close or exceeds the average spending of the other generations** despite there being less customers in that generation.", unsafe_allow_html=True)

        st.markdown("<h4>Catergory Level: Average Spending per Generation</h4>", unsafe_allow_html=True)
        cat_lvl_avg_spending_per_gen(c5_trans, "cluster5-category-avg", True)

        st.markdown("Doing a further examination into the specific categories, the graph shows that **all generations have a high average on Online Categories**. Furthermore, we see a **high average monthly spending on the Travel category for the Greatest Generation**, which shows a possible marketing angle the company could take for this generation in this cluster (or for that sole customer). Other than that, there is a more or less moderate spending on all categories which indicate that **even if this cluster doesn't spend that much, they still use their cards for any type of purchases** (whether it's online or physical).", unsafe_allow_html=True)

        st.markdown("<h4>Average Monthly Spending</h4>", unsafe_allow_html=True)
        plot_avg_monthly_spending(c5_trans, "cluster5-avg-spending")

        st.markdown("Overall, the **average monthly spending on digital categories** across the the whole timeline of the transaction history is **greater than** then physical categories. There is a particularly high spike on digital transactions in the month of January 2021, which may need further examination. The graph showcases that in some months, this cluster mainly uses their card for physical transactions but whenever they use it for these types of transactions, they spend little to none. However, **when they spend on digital categories, they seem to have an overall higher average monthly spending**. The company can take advantage of this by doing <u>promotions and deals for online transactions to further increase</u> the average monthly spending on these types of transactions.", unsafe_allow_html=True)
    
    st.subheader("Summary of Findings and Recommendations")
    st.markdown("To summarize, the KMeans clustering gave 6 unique clusters, each having their own RFM values. From there, 4 were named as the following:\n- Cyber Savvy Shoppers\n- Epic Comeback Connoisseurs\n- Digital Dynamos\n- Festive Spenders")

    st.markdown("From there, each cluster was further examined based on their spending. The following aspects were found:\n1. Cyber Savvy Shoppers\n\t- composed of 21 users and 27497 transactions\n\t- had a high average spending on digital transactions across all the generations\n\t\t- despite there being less customers in the Silent Generation than Baby Boomers age bracket, the digital spending of the Silent Generation is equal to that of the Baby Boomers\n\t- majority of the spendings are on online categories except for Grocery (they spend more on Physical Grocery over Online Grocery)\n\t- this cluster still spends a decent amount for physical categories\n\t- tend to spend more on October and in the Christmas season\n\t- **Recommendations:**\n\t\t- give enhanced cashback for online transactions which can be done through Cyber Monday or Black Friday\n\t\t- offer more promotions and offers for online products by partnering with E-Commerce platforms (free shipping, early access to products, exclusive deals, etc.) to encourage their online shopping\n\t\t- offer discounts and special deals during the Christmas season\n\t\t- partner with groceries for a customer loyalty program to encourage physical grocery shopping while encouraging them to make impulse purchases but also ensuring that you show care for the customers through coupons and rewards\n2. Epic Comeback Connoisseurs\n\t- composed of 12 users and 132 transactions\n\t\t- majority of which are part of the Baby Boomers while the rest of the generations had 2 users\n\t- generally had a high average spending on digital transactions but Generation X also had a high average spending on transactions part of the others category\n\t- majority of the spendings are on digital categories but overall, this cluster barely used their cards due to the little to no transactions on majority of the categories\n\t- this cluster has a declining trend in terms of average monthly spending\n\t\t- this indicates that as time passes by, this cluster uses their cards less or has the tendency to forget about using their cards\n\t- **Recommendations:**\n\t\t- give discounts for purchases made to popular retailers (especially for essentials) to encourage them to use their card more\n\t\t- offer free trials or samples for the categories they don't spend on such as Entertainment or Health and Fitness\n\t\t- offer cashback rewards during key dates (anniversaries, birthdays, holidays, etc.) to encourage them to keep their card active which serves as a reminder about the existence of the card\n3. Digital Dynamos", unsafe_allow_html=True)

elif my_page == "Summary":
    st.write('___')