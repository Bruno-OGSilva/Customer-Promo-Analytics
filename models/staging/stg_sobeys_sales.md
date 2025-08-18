# Staging Model: stg_sobeys_sales

## Overview
The `stg_sobeys_sales` model is responsible for extracting and transforming raw POS data for Sobeys. This data originates from CSV files obtained from major Canadian retailer portals. The model cleans and standardizes the data, ensuring that it is correctly formatted for further transformation using dbt core and analysis in Google BigQuery.

## Source Data
- **Source Table:** `source`
- **Original Columns:**
  - `store_id`
  - `Product`
  - `UPC No`
  - `Dollar Sales All Sales`
  - `Unit Sales All Sales`
  - `Time`
  - `retail_group`

## Transformations Applied
### Renaming Fields
- **UPC No → upc_no:** Retains the original UPC data.
- **Product:** Remains unchanged.
- **Dollar Sales All Sales → dollar_sales:** Represents the monetary sales value.
- **Unit Sales All Sales → unit_sales:** Represents the number of units sold.
- **Time → week_end_date:** Converted to a date type for consistent time-based analysis.

### Data Type Casting
- **UPC No as int → upc_int:** Ensures numeric operations can be performed on UPC values.
- **Dollar Sales All Sales as float64 → dollar_sales:** Provides precision for financial calculations.
- **Unit Sales All Sales as int64 → unit_sales:** Ensures integer consistency for unit counts.
- **Time as DATE → week_end_date:** Standardizes the date format for time-series analysis.

### Derived Fields
- **unique_store_id:** Created using `CONCAT(retail_group, '|', store_id)`, this field generates a unique identifier for each store by combining the `retail_group` and `store_id`. This facilitates reliable joining and aggregation in downstream models.
- **pod:**
  Created by concatenating `retail_group`, `Geography` and `UPC No` with a pipe (`|`) separator. This composite key will be used to calculate the point of ditribtuion KPI.

## Business Logic & Rationale
- **Data Consistency:** The transformations ensure that all data types are consistent and accurate, which is critical for analytical operations.
- **Improved Readability:** By renaming columns to more descriptive names (e.g., `store_name` and `week_end_date`), the model improves overall readability and maintainability.
- **Simplified Joins:** The creation of the `unique_store_id` simplifies downstream joins by providing a unique key for each store.
- **Preparation for Analysis:** These transformations lay the foundation for subsequent modeling layers (staging, intermediate, and mart) by ensuring that the raw data is clean and properly formatted.

## Model Dependencies
- **Upstream Data:** This model depends on the successful extraction of POS data from retailer CSV files and its subsequent loading into the raw `source` table.
- **Data Quality Checks:** Ensure that any changes in the CSV source schema are reflected in this model. Regular testing should verify the accuracy of data type conversions and transformations.

## Testing & Quality Assurance
- **Type Conversions:** Verify that the casting of `UPC No`, `Dollar Sales All Sales`, and `Unit Sales All Sales` is performed correctly.
- **Field Renaming:** Ensure that the original columns are correctly renamed to match the new naming conventions.
- **Derived Field Accuracy:** Validate that the `unique_store_id` is correctly concatenated from `retail_group` and `store_id`.
- **Data Integrity:** Employ dbt tests to check for nulls, data type mismatches, and other potential quality issues.

## Conclusion
The `stg_sobeys_sales` model is a critical first step in transforming raw POS data into a reliable, analyzable format. By applying necessary renaming, data type conversions, and deriving new fields, this model ensures that downstream analyses and business reporting are built on a foundation of clean and consistent data.
