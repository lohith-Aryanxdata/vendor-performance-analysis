import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db_connection import get_engine

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

engine = get_engine()

# 1. Vendor purchase performance
purchase_query = """
SELECT VendorNumber, TRIM(VendorName) AS VendorName,
       SUM(Quantity) AS total_qty,
       SUM(Dollars) AS total_purchase_dollars,
       COUNT(DISTINCT PONumber) AS total_orders
FROM purchases
GROUP BY VendorNumber, TRIM(VendorName)
ORDER BY total_purchase_dollars DESC;
"""
df_purchases = pd.read_sql(purchase_query, engine)

# 2. Vendor sales performance
sales_query = """
SELECT VendorNo, TRIM(VendorName) AS VendorName,
       SUM(SalesQuantity) AS total_sold_qty,
       SUM(SalesDollars) AS total_sales_dollars
FROM sales
GROUP BY VendorNo, TRIM(VendorName)
ORDER BY total_sales_dollars DESC;
"""
df_sales = pd.read_sql(sales_query, engine)

# 3. Freight % by vendor
freight_query = """
SELECT VendorNumber, TRIM(VendorName) AS VendorName,
       SUM(Freight) AS total_freight,
       SUM(Dollars) AS total_invoice_dollars,
       ROUND(SUM(Freight) / NULLIF(SUM(Dollars),0) * 100, 2) AS freight_pct
FROM vendor_invoice
GROUP BY VendorNumber, TRIM(VendorName)
ORDER BY freight_pct DESC;
"""
df_freight = pd.read_sql(freight_query, engine)

# 4. Lead time by vendor
leadtime_query = """
SELECT VendorNumber, TRIM(VendorName) AS VendorName,
       ROUND(AVG(DATEDIFF(ReceivingDate, PODate)), 1) AS avg_lead_time_days
FROM purchases
WHERE ReceivingDate IS NOT NULL AND PODate IS NOT NULL
GROUP BY VendorNumber, TRIM(VendorName)
ORDER BY avg_lead_time_days DESC;
"""
df_leadtime = pd.read_sql(leadtime_query, engine)

print("Top 5 vendors by purchase $:")
print(df_purchases.head())
print("\nTop 5 vendors by sales $:")
print(df_sales.head())
print("\nTop 5 vendors by freight %:")
print(df_freight.head())
print("\nTop 5 vendors by lead time:")
print(df_leadtime.head())

print("\nShapes:", df_purchases.shape, df_sales.shape, df_freight.shape, df_leadtime.shape)

# Merge into a single vendor-level summary table
vendor_summary = df_purchases.merge(
    df_sales, left_on="VendorNumber", right_on="VendorNo", how="outer", suffixes=("_purchase", "_sales")
)
vendor_summary = vendor_summary.merge(df_freight[["VendorNumber", "freight_pct"]], on="VendorNumber", how="left")
vendor_summary = vendor_summary.merge(df_leadtime[["VendorNumber", "avg_lead_time_days"]], on="VendorNumber", how="left")

# Clean up duplicate vendor name/number columns
vendor_summary["VendorNumber"] = vendor_summary["VendorNumber"].fillna(vendor_summary["VendorNo"])
vendor_summary["VendorName"] = vendor_summary["VendorName_purchase"].fillna(vendor_summary["VendorName_sales"])
vendor_summary = vendor_summary.drop(columns=["VendorNo", "VendorName_purchase", "VendorName_sales"])

# Drop any remaining exact duplicate rows just in case
vendor_summary = vendor_summary.drop_duplicates(subset=["VendorNumber", "VendorName"])

# Derived metrics
vendor_summary["gross_profit"] = vendor_summary["total_sales_dollars"] - vendor_summary["total_purchase_dollars"]
vendor_summary["profit_margin_pct"] = round(
    (vendor_summary["gross_profit"] / vendor_summary["total_sales_dollars"]) * 100, 2
)
vendor_summary["sell_through_pct"] = round(
    (vendor_summary["total_sold_qty"] / vendor_summary["total_qty"]) * 100, 2
)

# Reorder columns nicely
vendor_summary = vendor_summary[[
    "VendorNumber", "VendorName", "total_qty", "total_purchase_dollars",
    "total_orders", "total_sold_qty", "total_sales_dollars",
    "gross_profit", "profit_margin_pct", "sell_through_pct",
    "freight_pct", "avg_lead_time_days"
]]

vendor_summary = vendor_summary.sort_values("total_sales_dollars", ascending=False)

print("\n=== VENDOR SUMMARY (Top 10) ===")
print(vendor_summary.head(10))

# Save for reuse in charting script / report
os.makedirs("../data/processed", exist_ok=True)
vendor_summary.to_csv("../data/processed/vendor_summary.csv", index=False)
print("\nSaved vendor_summary.csv")
print("Total unique vendors in summary:", vendor_summary.shape[0])
# ============ CHARTS ============
sns.set_style("whitegrid")
os.makedirs("../docs/charts", exist_ok=True)

top10 = vendor_summary.head(10)

# 1. Top 10 vendors by sales $
plt.figure(figsize=(10,6))
sns.barplot(data=top10, y="VendorName", x="total_sales_dollars", palette="viridis")
plt.title("Top 10 Vendors by Sales Revenue")
plt.xlabel("Total Sales ($)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("../docs/charts/top10_vendors_sales.png", dpi=150)
plt.close()

# 2. Profit margin % distribution
plt.figure(figsize=(10,6))
sns.histplot(vendor_summary["profit_margin_pct"].dropna(), bins=30, kde=True, color="teal")
plt.title("Distribution of Vendor Profit Margin %")
plt.xlabel("Profit Margin %")
plt.tight_layout()
plt.savefig("../docs/charts/profit_margin_distribution.png", dpi=150)
plt.close()

# 3. Top 10 by profit margin (min $1M sales to avoid tiny-vendor noise)
significant = vendor_summary[vendor_summary["total_sales_dollars"] > 1_000_000]
top_margin = significant.sort_values("profit_margin_pct", ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(data=top_margin, y="VendorName", x="profit_margin_pct", palette="crest")
plt.title("Top 10 Vendors by Profit Margin % (Sales > $1M)")
plt.xlabel("Profit Margin %")
plt.ylabel("")
plt.tight_layout()
plt.savefig("../docs/charts/top10_profit_margin.png", dpi=150)
plt.close()

# 4. Freight % vs Lead time scatter
plt.figure(figsize=(10,6))
sns.scatterplot(data=vendor_summary, x="avg_lead_time_days", y="freight_pct", size="total_sales_dollars",
                 sizes=(20,400), alpha=0.6, legend=False)
plt.title("Freight % vs Lead Time by Vendor (bubble size = sales $)")
plt.xlabel("Average Lead Time (days)")
plt.ylabel("Freight %")
plt.tight_layout()
plt.savefig("../docs/charts/freight_vs_leadtime.png", dpi=150)
plt.close()

# 5. Sell-through % distribution
plt.figure(figsize=(10,6))
sns.histplot(vendor_summary["sell_through_pct"].clip(upper=150).dropna(), bins=30, color="orange")
plt.title("Distribution of Sell-Through % (clipped at 150%)")
plt.xlabel("Sell-Through %")
plt.tight_layout()
plt.savefig("../docs/charts/sell_through_distribution.png", dpi=150)
plt.close()

print("\nAll charts saved to docs/charts/")