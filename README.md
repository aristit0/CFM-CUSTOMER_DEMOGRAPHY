# Customer Demography Data Pipeline

This repository contains a complete streaming use case for generating, processing, and querying customer demographic data for banking applications.

## Components

- **MySQL** – Source database with three tables: `customer_info`, `bank_product`, and `customer_asset`.
- **Apache NiFi** – Used for Change Data Capture (CDC) from MySQL and flattening records.
- **Apache Phoenix** – Stores the flattened result in a single table: `CUSTOMER.CUSTOMER_DEMOGRAPHY`.
- **Flask** – Web application for querying customer data by CIF.

## Use Case Summary

Each customer has:

- 1 record in `customer_info`
- 1 record in `bank_product`
- 1 record in `customer_asset`

These are joined and stored as one row in `CUSTOMER.CUSTOMER_DEMOGRAPHY`.

## Phoenix Table Schema

```sql
CREATE TABLE CUSTOMER.CUSTOMER_DEMOGRAPHY (
  CIF BIGINT NOT NULL PRIMARY KEY,
  NAME VARCHAR,
  BIRTHDATE VARCHAR,
  GENDER VARCHAR,
  ADDRESS VARCHAR,
  CITY VARCHAR,
  PRODUCTID BIGINT,
  PRODUCTTYPE VARCHAR,
  OPENDATE VARCHAR,
  STATUS VARCHAR,
  ASSETID BIGINT,
  ASSETTYPE VARCHAR,
  ASSETVALUE DECIMAL,
  VALUATION_DATE VARCHAR
) SALT_BUCKETS=6, COMPRESSION='snappy';


## Data Generator

A Python script (`generated_customer_data.py`) simulates 5 million customers in MySQL. Each customer includes:

- 1 customer info record
- 1 linked bank product
- 1 linked asset

Data is inserted in batches of 1,000 with a 1-second delay per batch to simulate real-time ingestion.

### How to Run

```bash
cd data_generator
python3 generated_customer_data.py

## System Overview

This project demonstrates a unified real-time data processing pipeline designed to:

- Simulate real-world banking data generation
- Capture changes from MySQL in real-time using Apache NiFi
- Transform and flatten relational data across three source tables
- Store the output as a single record per customer in Apache Phoenix
- Allow fast querying via a simple Flask web app

---

## Data Flow Summary

1. **Data Generation (Python)**  
   Generates 5 million customer profiles and inserts them into MySQL in batches.

2. **Change Data Capture (NiFi)**  
   Uses the `CaptureChangeMySQL` processor to listen to MySQL binlog events from:
   - `customer_info`
   - `bank_product`
   - `customer_asset`

3. **Data Merging & Transformation (NiFi)**  
   - Events are grouped by `CIF` using `MergeRecord`
   - Flattened into a single JSON structure
   - Converted using `JsonTreeReader` and routed to `PutDatabaseRecord`

4. **Storage in Apache Phoenix**  
   - Flattened data is upserted into `CUSTOMER.CUSTOMER_DEMOGRAPHY`
   - Stored using snappy compression and SALT_BUCKETS for scalable read/write performance

5. **Query Interface (Flask)**  
   - Web app connects to Phoenix QueryServer using the thin client
   - End-user enters a `CIF`, and the app displays personal info, product, and asset

---

## Integration Highlights

- **Flattened Design**: Ensures 1 row per customer for fast OLAP-style analytics.
- **Upsert Safety**: Phoenix's `UPSERT` prevents duplicate CIF entries.
- **Timezone Compliance**: MySQL must be set to an IANA-compliant timezone (e.g., `Asia/Jakarta`) due to NiFi CDC limitations.
- **Modular Deployment**: Each component (generator, NiFi, Phoenix, Flask) can run independently or as part of a full pipeline.

---

## Use Cases

- Customer 360 views
- Real-time KYC profiling
- Transactional demography enrichment
- Front-office customer lookup interfaces