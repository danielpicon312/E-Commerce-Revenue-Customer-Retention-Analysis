# Online Retail II — Sales & Customer Revenue Dashboard

An end-to-end data analytics project using **Python**, **SQLite**, and **Power BI** to clean, model, and visualize two years of UK-based online retail transactions (December 2009 – December 2011).

![Dashboard Preview](dashboard.png)

## Key Metrics & Findings

* **Net Revenue (£18.86M):** Computed across all rows as \(\text{Net Revenue} = \sum (\text{Quantity} \times \text{Price})\). Negative quantities from returns and cancellations remain included so reported revenue reflects realized net sales rather than gross volume.
* **Order Value Skew (AOV £510.92 vs. MOV £302.22):** Average Order Value sits well above Median Order Value, indicating that high-value bulk or wholesale invoices pull the mean upward while a typical order sits closer to £302.
* **Seasonal Peaks:** Order counts and revenue build steadily through autumn and peak in **November**—reflecting combined monthly order activity across all available years in the dataset—before tapering in December.
* **Geographic Concentration:** Sales are heavily weighted toward the United Kingdom, followed by secondary European and international markets such as Ireland, the Netherlands, Germany, and France.
* **Guest vs. Registered Customers:** Orders with missing `Customer ID` values remain included in overall revenue, order counts, and order-value metrics, but are excluded from the **Top 10 Customers** visual so anonymous transactions are not misattributed to registered accounts.

## Tech Stack

* **ETL & Storage:** Python (`pandas`, `sqlite3`, `pathlib`), SQLite
* **BI & Modeling:** Power BI, DAX

## Repository Layout

```text
OnlineRetailIIUCI/
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
* **Missing Customer Handling:** Blank `Customer ID` records are preserved in the model so total revenue and order counts stay accurate while Top 10 customer rankings remain restricted to identified customers.
* **Scale & Formatting:** Monetary metrics are formatted in GBP (`£`), `InvoiceDate` uses the `Date` type to drive the date-range slicer and monthly trend visuals, and the revenue trend Y-axis is anchored at `£0.0M` to prevent visual distortion across filter selections.

## Report Structure

* **KPI Cards:** Net Revenue, Average Order Value, and Median Order Value.
* **Filters & Country Breakdown:** Country slicer, `InvoiceDate` range slider, and a country revenue summary table.
* **Trends & Seasonality:** Monthly revenue over time alongside combined multi-year monthly order counts.
* **Products & Customers:** Horizontal bar visuals for **Product Revenue** by cleaned `Description` (excluding postage and non-product fees) and **Top 10 Customers** (excluding guest checkouts).

## Local Setup

1. Place `online_retail_II.csv` in the same folder as `onlineretailanalysis.py`.
2. Install required Python packages:
   ```bash
   pip install pandas
   ```
3. Run the ETL script to generate `online_retail.db`:
   ```bash
   python onlineretailanalysis.py
   ```
4. Open `OnlineRetailAnalysis.pbix` in Power BI Desktop, point the SQLite ODBC connection (DSN or connection string) to your local `online_retail.db` if prompted, and refresh the data.