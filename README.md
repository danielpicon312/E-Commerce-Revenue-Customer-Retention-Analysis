# E-Commerce Sales & Customer Performance Analysis

![Dashboard Preview](dashboard.png)
[Note: This is a static preview. The full interactive Power BI dashboard (`.pbix`) is available in this repository for download and exploration.]

# Project Overview
For this project, I analyzed two years of e-commerce transaction data (covering December 1, 2009 through December 9, 2011) to get a clearer picture of overall revenue trends, order sizes, customer concentration, and where sales were coming from globally. Using SQLite3, pandas, Python, and Power BI, I cleaned up the raw transactional logs and built an executive dashboard tracking $19.29M in net revenue.

# Key Findings
Looking at the numbers, total net revenue came out to $19.29M over the two-year period. One of the most interesting takeaways was comparing the average transaction value ($523.30) to the median transaction value ($304.32). That gap shows the data is heavily right-skewed—while most everyday orders are relatively modest, a smaller number of massive wholesale or bulk orders pull the average way up.

Seasonality also played a huge role. Revenue followed a clear fourth-quarter cycle, surging past $1.4M per month in late Q4 of both 2010 and 2011 before dropping back down in January. (Note that December 2011 shows a sharp drop-off simply because the dataset cuts off on December 9.)

On the customer side, revenue among registered buyers was heavily concentrated at the top. Customer 18102 led all accounts at roughly $0.60M, followed closely by Customer 14646 at around $0.52M, with a steep drop-off across the rest of the top ten. Geographically, the vast majority of sales were concentrated in Europe—mostly the UK and neighboring countries—with smaller pockets of activity in North America, Asia, and Australia.

# How I Built It
Working with raw transactional data meant making a few deliberate cleaning and modeling choices before building the visuals:

Accounting for Returns: Instead of filtering out negative quantities and refunds, I kept them in the top-line calculations so the dashboard reflects true net revenue rather than inflated gross numbers. 
Handling Guest Checkouts: A large chunk of rows didn't have a Customer ID attached, representing guest checkouts. I kept those records in the dataset so total revenue and country breakdowns stayed accurate, but filtered them out of the Top 10 Customers visual so unattributed sales wouldn't lump together and take the #1 spot.

Data Modeling & DAX: I converted Customer IDs to text fields so Power BI wouldn't treat them as continuous numbers on an axis, and wrote distinct-order measures to calculate accurate mean and median values across multi-line invoices.

# Takeaways & Next Steps
Based on these patterns, a few practical next steps stand out for the business:

1. Protect Top Accounts: Since a handful of wholesale buyers account for a massive share of revenue, setting up dedicated account management or tiered loyalty perks for the top 10 customers (especially IDs 18102 and 14646) would help lock in that recurring spend.

2. Prepare Early for Q4: Because the October–November spike is so consistent year over year, inventory and fulfillment capacity should be scaled up in late Q3 to avoid bottlenecks.

3. Convert Guest Buyers: Offering a simple post-checkout incentive to create an account could help turn untraceable guest transactions into trackable, repeat customer relationships.
