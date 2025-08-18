# Staging Model: stg_ccl_sales

## Overview
The `stg_ccl_sales` model is responsible for extracting, cleaning, and transforming raw CCL sales data from the POS system. The data is sourced from the `raw_ccl_sales` table in the `pos` schema. This model renames columns, casts data types, and derives key identifiers to ensure the data is ready for downstream processing and analytics.

## Source Data
- **Source Table:** `pos.raw_ccl_sales`
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
  Remains unchanged.
- **UPC ID → upc_no:**
  Captures the original UPC identifier.
- **Dollar Sales → dollar_sales:**
  Represents the total sales in dollars.
- **Unit Sales → unit_sales:**
  Represents the count of units sold.
- **Time → week_end_date:**
  Converted to a date type for proper time-series analysis.

### Data Type Casting
- **UPC ID as int → upc_int:**
  The UPC identifier is also cast to an integer to facilitate numerical operations.
- **Dollar Sales as float64:**
  Ensures precision in financial calculations.
- **Unit Sales as int64:**
  Guarantees integer consistency for unit count analysis.
- **Time as DATE:**
  Standardizes the date format for time-based aggregations.

### Derived Field
- **unique_store_id:**
  Created by concatenating `retail_group` and `Geography` with a pipe (`|`) separator. This composite key uniquely identifies each store record, aiding in accurate joins and aggregations across models.
- **pod:**
  Created by concatenating `retail_group`, `Geography` and `UPC ID` with a pipe (`|`) separator. This composite key will be used to calculate the point of ditribtuion KPI.

## Business Logic & Rationale
- **Data Consistency:**
  By enforcing proper data types and standard naming conventions, the model ensures that the data is consistent and ready for analysis.
- **Clarity & Maintainability:**
  Renaming columns to more descriptive names (e.g., `store_id` and `week_end_date`) improves clarity for data analysts and maintains consistency across the data pipeline.
- **Unique Identification:**
  The creation of the `unique_store_id` field is critical for eliminating ambiguities and enabling reliable linking with other datasets.
- **Preparation for Downstream Processing:**
  These transformations lay the groundwork for more complex analytical models and reporting, ensuring that subsequent stages operate on clean, well-structured data.

## Dependencies & Testing Considerations
- **Dependencies:**
  This model depends on the raw data loaded into the `pos.raw_ccl_sales` table. Any changes to the source schema must be reflected in this model.
- **Recommended Tests:**
  - **Not Null Tests:** Verify that key fields such as `store_id`, `product`, `upc_no`, `upc_int`, `dollar_sales`, `unit_sales`, `week_end_date`, `retail_group`, and `unique_store_id` are not null.
  - **Data Type Validation:** Ensure that `upc_int`, `dollar_sales`, and `unit_sales` are correctly cast to their intended numeric types.

## Conclusion
The `stg_ccl_sales` model plays a crucial role in the data pipeline by transforming raw sales data into a standardized format. This model ensures that the data is clean, correctly typed, and uniquely identified, providing a solid foundation for further analytical processing and business intelligence activities.
