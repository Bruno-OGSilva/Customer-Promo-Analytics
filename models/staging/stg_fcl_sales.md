# Staging Model: stg_fcl_sales

## Overview
The `stg_fcl_sales` model is designed to extract, clean, and transform raw FCL sales data from the POS system. Sourced from the `pos.raw_fcl_sales` table, this model renames columns, casts data types, and creates derived fields to ensure the data is standardized and ready for downstream analytical processing.

## Source Data
- **Source Table:** `pos.raw_fcl_sales`
- **Raw Columns:**
  - `Store Number`
  - `Product Name`
  - `UPC`
  - `Dollar Sales`
  - `Unit Sales`
  - `Week End Date`
  - `retail_group`
  - `Promotion Type Name`

## Transformations Applied
### Column Renaming
- **`Store Number` → store_id:**
  Renames the column to serve as the primary identifier for each store.
- **`Product Name` → product:**
  Renames the product description for clarity.
- **`UPC` → upc_no:**
  Retains the original UPC value as a string.
- **`Promotion Type Name` → promo_type:**
  Renames the promotion type information for easier interpretation.

### Data Type Casting & Derived Fields
- **UPC Casting:**
  The `UPC` field is cast to an integer to create `upc_int` for numerical operations.
- **Dollar Sales:**
  Cast to `float64` to accurately represent monetary values as `dollar_sales`.
- **Unit Sales:**
  Cast to `int64` to ensure unit counts are stored as integers in `unit_sales`.
- **Week End Date:**
  Cast to a DATE type as `week_end_date` to facilitate time-series analysis.
- **Unique Store Identifier:**
  A new field, `unique_store_id`, is derived by concatenating `retail_group` and `Store Number` (i.e., `store_id`) with a pipe (`|`) separator. This composite key uniquely identifies each store record.
- **pod:**
  Created by concatenating `retail_group`, `Store Number` and `UPC` with a pipe (`|`) separator. This composite key will be used to calculate the point of ditribtuion KPI.

## Business Logic & Rationale
- **Data Consistency:**
  Standardizing column names and data types helps maintain consistent and reliable data across the pipeline.
- **Improved Clarity:**
  Renaming columns makes the data more intuitive and easier to understand for downstream users and analysts.
- **Accurate Analysis:**
  Casting monetary and unit fields to appropriate numeric types ensures precise financial and quantitative analysis.
- **Unique Identification:**
  The `unique_store_id` field is crucial for preventing duplicates and facilitating accurate joins with other datasets in later stages.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the integrity and schema of the `pos.raw_fcl_sales` table. Any changes in the raw data source must be reflected in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields such as `store_id`, `product`, `upc_no`, `dollar_sales`, `unit_sales`, `week_end_date`, and `unique_store_id` are not null.
  - **Data Type Verification:** Confirm that numeric fields (`upc_int`, `dollar_sales`, and `unit_sales`) are correctly cast.
  - **Uniqueness Test:** Verify that the `unique_store_id` is unique across all records to prevent duplication.

## Conclusion
The `stg_fcl_sales` model cleans and standardizes raw FCL sales data by applying a series of transformations including renaming, type casting, and unique identifier creation. This process ensures that the data is reliable and well-structured, providing a strong foundation for downstream reporting and business intelligence.
