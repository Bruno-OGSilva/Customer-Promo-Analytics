# Staging Model: stg_metro_sales

## Overview
The `stg_metro_sales` model is responsible for extracting, cleaning, and transforming raw Metro sales data from the POS system. This model pulls data from the `raw_metro_sales` table within the `pos` schema and applies a series of transformations—including renaming columns, casting data types, parsing dates, and generating a unique store identifier—to ensure the data is standardized and ready for further downstream processing and analysis.

## Source Data
- **Source Table:** `pos.raw_metro_sales`
- **Raw Columns:**
  - `Store No`
  - `Product`
  - `UPC ID`
  - `Dollar Sales`
  - `Unit Sales`
  - `Week End Date`
  - `retail_group`

## Transformations Applied
### Column Renaming
- **`Store No` → store_id:**
  Renames the original store identifier to `store_id` for clarity.
- **Product → product:**
  Retains the product information.
- **`UPC ID` → upc_no:**
  Keeps the original UPC identifier.
- **Additional Field Creation:**
  - **upc_int:**
    The `UPC ID` is also cast to an integer to create a new field (`upc_int`) to support numerical operations.

### Data Type Casting & Date Parsing
- **Dollar Sales → dollar_sales:**
  Cast as a `float64` to accurately represent monetary values.
- **Unit Sales → unit_sales:**
  Cast as an `int64` to ensure unit counts are maintained as integer values.
- **Week End Date → week_end_date:**
  Parsed using `PARSE_DATE('%m/%d/%Y', \`Week End Date\`)` to convert the string date into a proper DATE format, facilitating time-series analysis.

### Derived Field
- **unique_store_id:**
  A composite unique identifier is created by concatenating `retail_group` and `Store No` with a pipe (`|`) separator. This derived field is essential for ensuring each store record is uniquely identifiable, which simplifies downstream joins and aggregations.
  - **pod:**
  Created by concatenating `retail_group`, `Store No` and `UPC ID` with a pipe (`|`) separator. This composite key will be used to calculate the point of ditribtuion KPI.


## Business Logic & Rationale
- **Standardization:**
  Renaming columns and enforcing consistent data types makes the dataset easier to understand and use in later stages of the data pipeline.
- **Data Integrity:**
  By casting numeric fields and parsing dates correctly, the model ensures that data is both reliable and ready for accurate financial and temporal analyses.
- **Unique Identification:**
  The creation of `unique_store_id` is a key step in preventing duplicates and ensuring that each store's sales data can be uniquely joined with other datasets.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the raw data available in the `pos.raw_metro_sales` table. Any changes to the source schema should be reflected in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Verify that critical fields such as `store_id`, `product`, `upc_no`, `upc_int`, `dollar_sales`, `unit_sales`, `week_end_date`, and `unique_store_id` are not null.
  - **Data Type Verification:** Ensure that the data type conversions for numeric fields and date parsing are correct.
  - **Uniqueness Test:** Validate that the `unique_store_id` is unique across the dataset.

## Conclusion
The `stg_metro_sales` model transforms raw Metro sales data into a clean and structured format, ensuring consistency and reliability for downstream analysis. With proper renaming, data type casting, date parsing, and the generation of a store unique identifier, this model forms a robust foundation for subsequent reporting and business intelligence efforts.
