# Online Retail II — Sales & Customer Revenue Dashboard

An end-to-end data analytics project using **Python**, **SQLite**, and **Power BI** to clean, model, and visualize two years of UK-based online retail transactions (December 2009 – December 2011).

![Dashboard Preview](dashboard.png)

## Key Metrics & Findings

* **Net Revenue (£18.86M):** Computed across all rows as `Net Revenue = Σ(Quantity × Price)`. Negative quantities from returns and cancellations remain included so reported revenue reflects realized net sales rather than gross volume. Non-product rows in the source data (postage, fees, and manual or accounting adjustments) are also included in this total.
* **Order Value Skew (AOV £510.92 vs. MOV £302.22):** Average Order Value sits well above Median Order Value, indicating that high-value bulk or wholesale invoices pull the mean upward while a typical order sits closer to £302. Both figures are calculated over all invoices, including cancellation invoices with negative totals.
* **Seasonal Peaks:** Order counts and Net Revenue build steadily through autumn and peak in **November** before tapering in December. Comparing 24 full months, November averages the most orders of any month, while December falls back to roughly spring levels.
* **Geographic Concentration:** Sales are heavily weighted toward the United Kingdom, followed by secondary European and international markets such as Ireland, the Netherlands, Germany, and France.
* **Guest vs. Registered Customers:** Orders with missing `Customer ID` values remain included in overall Net Revenue, order counts, and order-value metrics, but are excluded from the **Top 10 Customers** visual so anonymous transactions are not misattributed to registered accounts.

## Business Recommendations

* **Plan inventory and marketing around the autumn ramp.** Demand climbs from September and peaks in November, so stock for top sellers and seasonal lines should be secured, and campaigns launched, before the ramp begins rather than during it.
* **Treat high-value buyers as a distinct segment.** The gap between average and median order value points to a group of bulk or wholesale customers. Tailored pricing, volume discounts, or account management could protect and grow this revenue.
* **Prioritize retention of top customers.** Revenue drops off steeply after the first few registered customers, and the top two each generated over £0.5M, so losing any one of them would be noticeable. These accounts are worth monitoring for drops in order frequency.
* **Test growth in secondary markets.** Revenue is concentrated in the UK. Ireland, the Netherlands, Germany, and France already generate meaningful sales and are natural candidates for targeted expansion.

## Data Source

This project uses the **Online Retail II** dataset from the UCI Machine Learning Repository: <https://archive.ics.uci.edu/dataset/502/online+retail+ii>

> Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D

The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). UCI distributes it as an Excel workbook (`online_retail_II.xlsx`) with one sheet per year; combine both sheets and save them as `online_retail_II.csv` before running the ETL script. The raw data and the generated database are not committed to this repository.

## Data Notes & Limitations

* **Monthly order counts use 24 full months.** The **Order Count by Month** chart is filtered to December 2009 – November 2011, so every calendar month appears exactly twice and the bars are directly comparable. The partial December 2011 (through December 9) is excluded from this chart only; all other visuals use the full dataset.
* **Net Revenue includes non-product rows.** Postage, fees, and manual or accounting adjustments are part of the £18.86M total. They are excluded only from the **Product Revenue** chart.
* **Order-value metrics include cancellations.** Cancellation invoices carry negative totals and are included in Average and Median Order Value, which pulls both figures slightly down.

## Tech Stack

* **ETL & Storage:** Python (`pandas`, `sqlite3`, `pathlib`), SQLite
* **BI & Modeling:** Power BI, DAX

## Repository Layout

```text
E-Commerce-Revenue-Customer-Retention-Analysis/
├── README.md
├── .gitignore
├── .gitattributes
├── onlineretailanalysis.py
├── OnlineRetailAnalysis.pbix
└── dashboard.png
```

## ETL Pipeline (`onlineretailanalysis.py`)

* Reads `online_retail_II.csv` from the project directory, trims column header whitespace, and removes duplicate rows.
* Casts `Customer ID` to pandas nullable `Int64` (stripping `.0` decimals while preserving missing values), then stores it as `TEXT` in SQLite.
* Builds the `invoices` table via SQL with `SELECT DISTINCT`, trims product text via `TRIM(Description)`, and standardizes country labels (`EIRE` → `Ireland`, `RSA` → `South Africa`, `Unspecified` → `Unknown`).
* Drops `raw_invoices`, commits changes, and runs `VACUUM` to reclaim disk space in `online_retail.db`.

## Power BI & DAX Design

* **Invoice-Level Aggregations:** Average Order Value and Median Order Value evaluate over `VALUES(invoices[Invoice])` (`AVERAGEX` / `MEDIANX`) so orders with multiple line items are not double-counted as separate orders.
* **Product-Level Filtering:** Non-merchandise accounting and shipping items (such as `DOTCOM POSTAGE` and `POSTAGE`) are excluded at the visual level in the **Product Revenue** chart so top-product rankings highlight physical goods while keeping shipping fees intact in overall Net Revenue.
* **Seasonality Comparison Window:** A visual-level filter limits **Order Count by Month** to `InvoiceDate` on or after 1 December 2009 and before 1 December 2011. Without it, December would combine three years (one partial) against two for every other month. The upper bound uses *before 1 December* rather than *on or before 30 November* because `InvoiceDate` includes a time, so the latter would drop orders placed during 30 November.
* **Missing Customer Handling:** Blank `Customer ID` records are preserved in the model so total Net Revenue and order counts stay accurate while Top 10 customer rankings remain restricted to identified customers.
* **Scale & Formatting:** Monetary metrics are formatted in GBP (`£`), `InvoiceDate` uses the `Date` type to drive the date-range slicer and monthly trend visuals, and the Net Revenue trend Y-axis is anchored at `£0.0M` to prevent visual distortion across filter selections.

## Report Structure

* **KPI Cards:** Net Revenue, Average Order Value, and Median Order Value.
* **Filters & Country Breakdown:** Country slicer, `InvoiceDate` range slider, and a country Net Revenue summary table.
* **Trends & Seasonality:** Monthly Net Revenue over time alongside order counts by calendar month across 24 full months (December 2009 – November 2011).
* **Products & Customers:** Horizontal bar visuals for **Product Revenue** by cleaned `Description` (excluding postage and non-product fees) and **Top 10 Customers** (excluding guest checkouts).

## Local Setup

1. Download the dataset (see [Data Source](#data-source)) and place `online_retail_II.csv` in the same folder as `onlineretailanalysis.py`.
2. Install required Python packages:
   ```bash
   pip install pandas
   ```
3. Run the ETL script to generate `online_retail.db`:
   ```bash
   python onlineretailanalysis.py
   ```
4. Open `OnlineRetailAnalysis.pbix` in Power BI Desktop, point the SQLite ODBC connection (DSN or connection string) to your local `online_retail.db` if prompted, and refresh the data.