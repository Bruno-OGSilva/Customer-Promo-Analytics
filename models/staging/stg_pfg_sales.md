# Staging Model: stg_pfg_sales

## Overview
The `stg_pfg_sales` model is responsible for transforming raw PFG sales data from the POS system. It extracts data from the `raw_pfg_sales` source in the `pos` schema, applies necessary transformations such as renaming columns, casting data types, and deriving unique identifiers. This prepares the data for reliable downstream processing and analysis.

## Source Data
- **Source Table:** `pos.raw_pfg_sales`
- **Raw Columns:**
  - `Geography`
  - `Product`
  - `UPC ID`
  - `Dollar Sales`
  - `Unit Sales`
  - `Time`
  - `retail_group`

## Transformations Applied
### Column Renaming
- **Geography → store_id:**
  The `Geography` column is repurposed to serve as the store identifier.
- **Product:**
  Remains unchanged, representing the product details.
- **UPC ID → upc_no:**
  Captures the original UPC identifier.
- **Dollar Sales → dollar_sales:**
  Represents the total sales amount in dollars.
- **Unit Sales → unit_sales:**
  Represents the number of units sold.
- **Time → week_end_date:**
  Converted to a DATE type to standardize the sales period.
- **retail_group:**
  Retained as-is for further categorization.

### Data Type Casting
- **UPC ID as int → upc_int:**
  Casting the `UPC ID` to an integer allows for numerical operations and comparisons.
- **Dollar Sales as float64:**
  Ensures precise financial calculations.
- **Unit Sales as int64:**
  Guarantees the consistency of unit sales as integer values.
- **Time as DATE:**
  Standardizes the date format, facilitating time-based analyses.

### Derived Field
- **unique_store_id:**
  Created by concatenating `retail_group` and the original `Geography` value (using a pipe `|` separator), this composite key uniquely identifies each store record. This is crucial for accurate joins and aggregations in subsequent models.
  - **pod:**
  Created by concatenating `retail_group`, `Geography` and `UPC ID` with a pipe (`|`) separator. This composite key will be used to calculate the point of ditribtuion KPI.

## Business Logic & Rationale
- **Data Standardization:**
  By enforcing consistent naming conventions and data types, the model ensures that the dataset is reliable and easy to work with for downstream analytics.
- **Unique Identification:**
  The derivation of `unique_store_id` guarantees that each store record is uniquely identifiable, reducing the risk of duplicates during data integration.
- **Preparation for Analysis:**
  These transformations cleanse and structure the raw data, providing a solid foundation for further business intelligence and analytical processing.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the integrity of data loaded into the `pos.raw_pfg_sales` table. Any changes in the raw data schema should be reflected here.
- **Quality Assurance:**
  It is recommended to implement tests to:
  - Ensure critical fields such as `store_id`, `product`, `upc_no`, `upc_int`, `dollar_sales`, `unit_sales`, `week_end_date`, and `unique_store_id` are not null.
  - Validate that data type conversions (for example, casting `UPC ID` to `upc_int`) are successful.
  - Verify that the `unique_store_id` is indeed unique across all records.

## Conclusion
The `stg_pfg_sales` model is a critical step in the data pipeline, transforming raw POS data into a structured, consistent format. These transformations support accurate and efficient downstream analysis, enabling robust business insights and decision-making.
