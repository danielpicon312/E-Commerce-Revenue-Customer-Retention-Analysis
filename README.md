# Online Retail II Sales & Customer Dashboard

This project cleans and analyzes transactional retail data from the Online Retail II dataset (`12/1/2009 – 12/9/2011`). A Python and SQLite pipeline processes the raw CSV into a local database, which feeds a Power BI dashboard built to track net revenue, order values, seasonality, and top accounts.

![Dashboard Preview](images/dashboard_preview.png)

## Overview & Key Numbers

* **Net Revenue:** £18.85M, calculated as $\text{Net Revenue} = \sum(\text{Quantity} \times \text{Price})$ across all records, including negative quantities from returns and cancellations.
* **Average Order Value (AOV):** £510.91
* **Median Order Value (MOV):** £302.22
* **Seasonality:** Order volume and revenue both peak in November before dropping off in December. Note that the seasonal order count chart combines monthly observations across all available years in the dataset.
* **Geography:** The UK accounts for most of the revenue, followed by Ireland, the Netherlands, Germany, and France.

## Tools Used

* Python (`pandas`, `sqlite3`, `pathlib`)
* SQLite
* Power BI & DAX

## Data Cleaning & Setup (`onlineretailanalysis.py`)

The onlineretailanalysis script reads `online_retail_II.csv` and builds `online_retail.db`:

1. Strips extra whitespace from column names and drops duplicate rows.
2. Casts `Customer ID` to nullable integers (`Int64`) so trailing `.0` decimals are removed without breaking null rows, then converts them to `TEXT` in SQLite.
3. Standardizes inconsistent country names in SQL (`EIRE` to `Ireland`, `RSA` to `South Africa`, `Unspecified` to `Unknown`).
4. Deduplicates records into a clean `invoices` table, drops the staging table, and runs `VACUUM` to keep the database compact.

## Power BI & DAX Notes

* **Invoice-level AOV & MOV:** Instead of averaging line items, `AOV` and `MOV` use `AVERAGEX` and `MEDIANX` over `VALUES(invoices[Invoice])` so every invoice is weighted once.
* **Null Customer IDs:** Rows without a `Customer ID` (unregistered/guest orders) are kept in all revenue, order count, AOV, and MOV calculations, but excluded from the Top 10 Customers chart so they don't distort individual customer rankings.
* **Formatting:** All currency values are formatted in GBP (`£`), and `InvoiceDate` is typed as `Date` for the date range slicer and monthly trend analysis.

## Dashboard Layout

* **Top Row:** Headline KPI cards for Net Revenue, Average Order Value, and Median Order Value.
* **Left Panel:** Multi-select Country slicer, Invoice Date slider, and a summary table of revenue by country.
* **Middle Row:** Monthly revenue trend over time alongside a seasonal order count chart combined across all years.
* **Bottom Row:** Horizontal bar charts ranking product revenue by `StockCode` and the Top 10 registered customers.

## Running Locally

1. Place `online_retail_II.csv` in the same directory as `onlineretailanalysis.py`.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the onlineretailanalysis pipeline to generate `online_retail.db`:
   ```bash
   python onlineretailanalysis.py
   ```
4. Open `powerbi/OnlineRetailDashboard.pbix` in Power BI Desktop.
5. If prompted, configure the SQLite ODBC connection (or update your local ODBC DSN/connection string) to point to the newly generated `online_retail.db`.
6. Refresh the report to load the latest data.