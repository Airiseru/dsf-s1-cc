# Project: Credit Card Analysis of Adobo Advantage Cards (AAC)

This was a project done inline with Eskwelab's Data Science Fellowship Cohort 13. However, only the `cc_dirty.csv` dataset came from Eskwelab. All codes, images, and presentation were done by me and my groupmates.

## Objectives

The main objective of the project is to learn more about a bank's customers based on their transaction history. Specifically, we look at what the company can do to improve their businesses based on the different type of customers they have. This was done by analyzing their RFM (Recency, Frequency, Monetary) values and perform clustering from those values. After which, specific action plans or recommendations were made for each cluster.

To learn more about the methodology, the [Jupyter Notebook](https://github.com/Airiseru/dsf-s1-cc/blob/main/cc-project-nb.ipynb) or [Streamlit App]() is available for viewing.

## Results

Using KMeans Clustering, it was discovered that 6 groups (or clusters) of customers were identified, each group having unique mean RFM values. The table shows the summary of the RFM values of each cluster made by the model.

| Cluster | Recency Value | Frequency Value | Monetary Value |
| ------- | ------------- | --------------- | -------------- |
| 0       | Low (316)     | Low (8)         | Low (5,382)    |
| 1       | High (25)     | High (1,309)    | High (91,383)  |
| 2       | Medium (124)  | Low (11)        | Low (5,136)    |
| 3       | High (25)     | Very High (1,957)| Very High (133,899) |
| 4       | Low (604)     | Low (8)         | Low (4,434)    |
| 5       | High (25)     | Medium (656)    | Medium (45,917)|

From the tables, we see that clusters 0 and 4 had little to no engagement (indicated by the high recency value, low frequency value, and low monetary value). Thus, the analysis will be focused on the remaining clusters instead as they have a higher potential for the company. That is, it is more beneficial if the company focuses their resources on them as they are already engaged, so the company only needs to focus on making them more engaged rather than trying to bring back their engagement.

### Cluster 1 -- Cyber Savvy Shoppers

In this cluster, customers tend to spend more on digital categories especially in the month of October. It is recommended to give these customers enhanced cashback on online transactions to encourage them to continue spending online. This can be done through Cyber Monday or Black Friday Bonuses where extra rewards are provided during these peak shopping seasons.

The company should also partner with E-Commerce platforms to offer exclusive deals to products, free shipping, or early access to new products to further encourage their online spending and enhance their online shopping experience.

### Cluster 2 -- Epic Comeback Connoisseurs

For this group, although they have low spending, they recently used their card for a purchase. This tells AAC that they can encourage these customers to spend using their card. It is recommended to give "Epic Comeback Exclusive Deals" for these customers such as discounts for purchases made to popular retailers and free trials. AAC can also offer cashback rewards during key dates such as anniversaries or birthdays to encourage them to keep their card active and purchase using that card.

### Cluster 3 -- Digital Dynamos

This group of customers are frequent users of the card and tend to buy expensive items, which makes them an elite tier of customers. For this group, it is recommended for the customers to offer double points on digital purchases and personalized online offers based on the platform and the categories they frequently purchase.

They can offer customized benefits such as discounts on luxury goods and services, provide upgrades to first-class travel, hotels, etc. This can be done by partnering with premium brands and services. AAC can also host exclusive or private networking events, parties, or even seminars for their elite customers to create a sense of exclusivity and value for these elite customers.

### Cluster 5 -- Festive Spenders

In this cluster, customers frequently spend but not on luxury brands or expensive purchases. For this case, it is recommended to offer holiday deals or seasonal promotions as they love spending during the holidays. The company can also offer discounts on essential services such as internet subscriptions to capitalize on the cluster's spending habits on essential items.
