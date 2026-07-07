import os
import mysql.connector
from dotenv import load_dotenv

# Resolve paths relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "..", ".env")
data_folder = os.path.join(script_dir, "..", "data")

load_dotenv(dotenv_path)

print("HOST:", os.getenv("MYSQL_HOST"))
print("USER:", os.getenv("MYSQL_USER"))
print("DB:", os.getenv("MYSQL_DB"))

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB"),
    allow_local_infile=True
)
cursor = conn.cursor()
cursor.execute("SET GLOBAL local_infile = 1;")

tables = {
    "begin_inventory.csv": {
        "table": "begin_inventory",
        "columns": "InventoryId, Store, City, Brand, Description, Size, onHand, Price, startDate"
    },
    "end_inventory.csv": {
        "table": "end_inventory",
        "columns": "InventoryId, Store, City, Brand, Description, Size, onHand, Price, endDate"
    },
    "purchase_prices.csv": {
        "table": "purchase_prices",
        "columns": "Brand, Description, Price, Size, Volume, Classification, PurchasePrice, VendorNumber, VendorName"
    },
    "purchases.csv": {
        "table": "purchases",
        "columns": ("InventoryId, Store, Brand, Description, Size, VendorNumber, VendorName, "
                    "PONumber, PODate, ReceivingDate, InvoiceDate, PayDate, PurchasePrice, "
                    "Quantity, Dollars, Classification")
    },
    "sales.csv": {
        "table": "sales",
        "columns": ("InventoryId, Store, Brand, Description, Size, SalesQuantity, SalesDollars, "
                    "SalesPrice, SalesDate, Volume, Classification, ExciseTax, VendorNo, VendorName")
    },
    "vendor_invoice.csv": {
        "table": "vendor_invoice",
        "columns": "VendorNumber, VendorName, InvoiceDate, PONumber, PODate, PayDate, Quantity, Dollars, Freight, @approval",
        "set_clause": "SET Approval = NULLIF(@approval, '')"
    },
}

for filename, info in tables.items():
    path = os.path.join(data_folder, filename).replace("\\", "/")
    table = info["table"]
    columns = info["columns"]
    set_clause = info.get("set_clause", "")

    query = f"""
        LOAD DATA LOCAL INFILE '{path}'
        INTO TABLE {table}
        FIELDS TERMINATED BY ','
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 ROWS
        ({columns})
        {set_clause};
    """
    print(f"Loading {filename} into {table} ...")
    cursor.execute(query)
    conn.commit()
    print(f"  -> {cursor.rowcount} rows loaded")

cursor.close()
conn.close()
print("All tables loaded successfully.")