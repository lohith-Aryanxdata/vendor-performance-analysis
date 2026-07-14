# Vendor Performance Analysis Report

## Overview
This analysis evaluates vendor performance across purchasing, sales, freight cost efficiency,
and delivery lead time using data from begin_inventory, end_inventory, purchases, purchase_prices,
vendor_invoice, and sales tables (loaded into MySQL, ~131 unique vendors, ~12.8M sales records,
~2.3M purchase records).

## Key Findings

### 1. Top Vendors by Revenue
Diageo North America leads by a wide margin ($68.7M in sales), followed by Martignetti Companies
($41.0M) and Pernod Ricard USA ($32.3M). These top 5 vendors account for a significant share of
total vendor revenue.

### 2. Profit Margin Leaders
While Diageo is the largest by volume, Constellation Brands Inc has the best profit margin among
high-volume vendors (36.35%), followed by E & J Gallo Winery (33.77%) — suggesting margin
performance doesn't always track with volume, and smaller-volume high-margin vendors may deserve
more strategic attention.

### 3. Freight Cost Efficiency
Freight cost as a percentage of invoice dollars is remarkably consistent across vendors
(~0.5%), indicating no vendor is disproportionately burdening the business with shipping costs.

### 4. Delivery Lead Time
Average lead times range from ~7-13 days across vendors, with Flavor Essence Inc showing the
longest average lead time (13 days). No extreme outliers were found, suggesting a generally
reliable vendor delivery network.

### 5. Sell-Through Rate
Most vendors show sell-through rates near 95-100%, meaning inventory purchased is largely sold
within the period. A few vendors (e.g., Bacardi USA at 102%) exceed 100%, which reflects sales
drawing down from beginning inventory rather than a data error.

## Data Quality Notes
- Vendor names contained inconsistent trailing whitespace, which caused duplicate groupings during
  aggregation — resolved using SQL `TRIM()`.
- A small number of Brand/VendorNumber values exist in `purchases`/`sales` without a matching
  record in `purchase_prices`/`vendor_invoice` — expected in real-world vendor data, tracked via
  orphan-record checks rather than enforced foreign keys.

## Recommendations
- Prioritize deeper relationships with high-margin vendors (Constellation Brands, E&J Gallo) even
  though they're not the top-volume vendors.
- Freight costs are well-controlled; no immediate vendor renegotiation needed on this front.
- Monitor vendors with longer lead times (Flavor Essence Inc, Aaper Alcohol) for potential supply
  chain risk.

## Charts
See `docs/charts/` for supporting visualizations:
- top10_vendors_sales.png
- profit_margin_distribution.png
- top10_profit_margin.png
- freight_vs_leadtime.png
- sell_through_distribution.png