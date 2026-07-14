CREATE DATABASE IF NOT EXISTS vendor_performance;
USE vendor_performance;

DROP TABLE IF EXISTS begin_inventory;
CREATE TABLE begin_inventory (
    InventoryId VARCHAR(30),
    Store       INT,
    City        VARCHAR(50),
    Brand       INT,
    Description VARCHAR(100),
    Size        VARCHAR(20),
    onHand      INT,
    Price       DECIMAL(10,2),
    startDate   DATE,
    INDEX idx_brand (Brand),
    INDEX idx_store (Store)
);

DROP TABLE IF EXISTS end_inventory;
CREATE TABLE end_inventory (
    InventoryId VARCHAR(30),
    Store       INT,
    City        VARCHAR(50),
    Brand       INT,
    Description VARCHAR(100),
    Size        VARCHAR(20),
    onHand      INT,
    Price       DECIMAL(10,2),
    endDate     DATE,
    INDEX idx_brand (Brand),
    INDEX idx_store (Store)
);

DROP TABLE IF EXISTS purchase_prices;
CREATE TABLE purchase_prices (
    Brand          INT,
    Description    VARCHAR(100),
    Price          DECIMAL(10,2),
    Size           VARCHAR(20),
    Volume         INT,
    Classification INT,
    PurchasePrice  DECIMAL(10,2),
    VendorNumber   INT,
    VendorName     VARCHAR(100),
    INDEX idx_brand (Brand),
    INDEX idx_vendor (VendorNumber)
);

DROP TABLE IF EXISTS vendor_invoice;
CREATE TABLE vendor_invoice (
    VendorNumber INT,
    VendorName   VARCHAR(100),
    InvoiceDate  DATE,
    PONumber     INT,
    PODate       DATE,
    PayDate      DATE,
    Quantity     INT,
    Dollars      DECIMAL(12,2),
    Freight      DECIMAL(10,2),
    Approval     DECIMAL(10,2),
    INDEX idx_vendor (VendorNumber)
);

DROP TABLE IF EXISTS purchases;
CREATE TABLE purchases (
    InventoryId     VARCHAR(30),
    Store           INT,
    Brand           INT,
    Description     VARCHAR(100),
    Size            VARCHAR(20),
    VendorNumber    INT,
    VendorName      VARCHAR(100),
    PONumber        INT,
    PODate          DATE,
    ReceivingDate   DATE,
    InvoiceDate     DATE,
    PayDate         DATE,
    PurchasePrice   DECIMAL(10,2),
    Quantity        INT,
    Dollars         DECIMAL(12,2),
    Classification  INT,
    INDEX idx_brand (Brand),
    INDEX idx_vendor (VendorNumber)
);

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    InventoryId     VARCHAR(30),
    Store           INT,
    Brand           INT,
    Description     VARCHAR(100),
    Size            VARCHAR(20),
    SalesQuantity   INT,
    SalesDollars    DECIMAL(12,2),
    SalesPrice      DECIMAL(10,2),
    SalesDate       DATE,
    Volume          DECIMAL(10,2),
    Classification  INT,
    ExciseTax       DECIMAL(10,2),
    VendorNo        INT,
    VendorName      VARCHAR(100),
    INDEX idx_brand (Brand),
    INDEX idx_vendor (VendorNo)
);