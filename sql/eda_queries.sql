USE vendor_performance;

-- Date ranges — confirm data covers what we expect
SELECT MIN(PODate), MAX(PODate) FROM purchases;
SELECT MIN(SalesDate), MAX(SalesDate) FROM sales;

-- Distinct vendors, brands, stores
SELECT COUNT(DISTINCT VendorNumber) AS vendor_count FROM purchases;
SELECT COUNT(DISTINCT Brand) AS brand_count FROM purchases;
SELECT COUNT(DISTINCT Store) AS store_count FROM purchases;
----------------------------------------------
-- Brands in purchases but missing from purchase_prices
SELECT COUNT(DISTINCT p.Brand) AS orphan_brands
FROM purchases p
LEFT JOIN purchase_prices pp ON p.Brand = pp.Brand
WHERE pp.Brand IS NULL;

-- Vendors in sales but missing from vendor_invoice
SELECT COUNT(DISTINCT s.VendorNo) AS orphan_vendors
FROM sales s
LEFT JOIN vendor_invoice vi ON s.VendorNo = vi.VendorNumber
WHERE vi.VendorNumber IS NULL;
----------------------------------------------
-- Total purchase $ and quantity per vendor
SELECT VendorNumber, VendorName,
       SUM(Quantity) AS total_qty,
       SUM(Dollars) AS total_purchase_dollars,
       COUNT(DISTINCT PONumber) AS total_orders
FROM purchases
GROUP BY VendorNumber, VendorName
ORDER BY total_purchase_dollars DESC
LIMIT 20;
-------------------------------------------
---Vendor sales perfomance
SELECT VendorNo, VendorName,
       SUM(SalesQuantity) AS total_sold_qty,
       SUM(SalesDollars) AS total_sales_dollars
FROM sales
GROUP BY VendorNo, VendorName
ORDER BY total_sales_dollars DESC
LIMIT 20;
----------------------------------------
---Freight cost as % of purchase dollars
SELECT vi.VendorNumber, vi.VendorName,
       SUM(vi.Freight) AS total_freight,
       SUM(vi.Dollars) AS total_invoice_dollars,
       ROUND(SUM(vi.Freight) / NULLIF(SUM(vi.Dollars),0) * 100, 2) AS freight_pct
FROM vendor_invoice vi
GROUP BY vi.VendorNumber, vi.VendorName
ORDER BY freight_pct DESC
LIMIT 20;
-------------------------------------------------
----Lead time analysis
SELECT VendorNumber, VendorName,
       ROUND(AVG(DATEDIFF(ReceivingDate, PODate)), 1) AS avg_lead_time_days,
       MIN(DATEDIFF(ReceivingDate, PODate)) AS min_lead_time,
       MAX(DATEDIFF(ReceivingDate, PODate)) AS max_lead_time
FROM purchases
WHERE ReceivingDate IS NOT NULL AND PODate IS NOT NULL
GROUP BY VendorNumber, VendorName
ORDER BY avg_lead_time_days DESC
LIMIT 20;
----------------------------------------------------
-----Margin: purchase price vs actual sales price, by brand/vendor
SELECT pp.Brand, pp.Description, pp.VendorName,
       pp.PurchasePrice,
       AVG(s.SalesPrice) AS avg_sales_price,
       ROUND(AVG(s.SalesPrice) - pp.PurchasePrice, 2) AS unit_margin,
       ROUND((AVG(s.SalesPrice) - pp.PurchasePrice) / NULLIF(pp.PurchasePrice,0) * 100, 2) AS margin_pct
FROM purchase_prices pp
JOIN sales s ON pp.Brand = s.Brand
GROUP BY pp.Brand, pp.Description, pp.VendorName, pp.PurchasePrice
ORDER BY margin_pct ASC
LIMIT 20;
-----------------------------------------------
-----Slow-moving inventory
SELECT e.Brand, e.Description, e.Store,
       e.onHand AS ending_stock,
       COALESCE(SUM(s.SalesQuantity), 0) AS total_sold
FROM end_inventory e
LEFT JOIN sales s ON e.Brand = s.Brand AND e.Store = s.Store
GROUP BY e.Brand, e.Description, e.Store, e.onHand
HAVING total_sold = 0 OR e.onHand > total_sold * 2
ORDER BY ending_stock DESC
LIMIT 20;
-----------------------------------------
---Inventory turnover 
SELECT 
    b.Brand, 
    b.Description,
    b.onHand AS begin_stock,
    e.onHand AS end_stock,
    COALESCE(p_totals.total_purchased, 0) AS purchased_qty,
    COALESCE(s_totals.total_sold, 0) AS sold_qty
FROM begin_inventory b
JOIN end_inventory e 
    ON b.Brand = e.Brand AND b.Store = e.Store
LEFT JOIN (
    SELECT Brand, Store, SUM(Quantity) AS total_purchased
    FROM purchases
    GROUP BY Brand, Store
) p_totals ON b.Brand = p_totals.Brand AND b.Store = p_totals.Store
LEFT JOIN (
    SELECT Brand, Store, SUM(SalesQuantity) AS total_sold
    FROM sales
    GROUP BY Brand, Store
) s_totals ON b.Brand = s_totals.Brand AND b.Store = s_totals.Store
LIMIT 20;
-------------------------------------------