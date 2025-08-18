# Intermediate Model: int_fcl_sales

## Overview
The `int_fcl_sales` model is an intermediate transformation layer that refines raw FCL sales data from the staging layer (`stg_fcl_sales`). In this model, the `promo_type` column is intentionally excluded because it is not common to other retail accounts. This adjustment ensures that when the sales data from various retail accounts is appended in the Mart layer, the schema remains consistent across all sources.

## Source Data
- **Source Model:** `stg_fcl_sales`
- **Key Columns from Source:**
  - `store_id`
  - `product`
  - `upc_no`
  - `upc_int`
  - `dollar_sales`
  - `unit_sales`
  - `week_end_date`
  - `retail_group`
  - `unique_store_id`
  - `pod`
  - `promo_type` (this column is excluded)

## Transformations Applied
- **Column Exclusion:**
  The model excludes the `promo_type` column, which is specific to FCL and not present in other retail accounts. This is done to maintain a consistent schema for the Mart layer where sales data from multiple retail sources will be appended.

- **Field Selection:**
  The following fields are selected from `stg_fcl_sales`:
  - **store_id:** Unique identifier for each store.
  - **product:** Product description.
  - **upc_no:** Original UPC number.
  - **upc_int:** UPC number cast as an integer.
  - **dollar_sales:** Sales amount in dollars, cleaned and cast to a numeric type.
  - **unit_sales:** Number of units sold, cast to an integer.
  - **week_end_date:** The end date of the sales week, cast to a DATE.
  - **retail_group:** Retail group classification.
  - **unique_store_id:** Composite unique identifier created by concatenating `retail_group` and `store_id`.
  - **pod:** Extended unique identifier combining `retail_group`, `store_id`, and `UPC`.

## Business Logic & Rationale
- **Consistent Schema for Aggregation:**
  Removing the `promo_type` column ensures that the sales data from FCL aligns with the data schema of other retail accounts, which is critical when all sales tables are appended in the Mart layer.

- **Simplification for Downstream Processing:**
  By standardizing the dataset to include only common fields, the model simplifies data integration and aggregation across different retail accounts.

- **Data Standardization:**
  The intermediate layer enforces a consistent set of fields that support reliable comparison and aggregation in later stages of the analytics pipeline.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the successful execution of the `stg_fcl_sales` model. Any changes in the staging model’s schema should be reflected here.

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that essential fields (`store_id`, `product`, `upc_no`, `upc_int`, `dollar_sales`, `unit_sales`, `week_end_date`, `retail_group`, `unique_store_id`, and `pod`) are not null.
  - **Schema Consistency:** Validate that the schema of the output aligns with the expected structure for the Mart layer.
  - **Exclusion Verification:** Confirm that the `promo_type` column is successfully excluded from the output.

## Conclusion
The `int_fcl_sales` model streamlines the raw FCL sales data by removing the `promo_type` column, ensuring a unified schema for the final Mart layer. This intermediate transformation is vital for creating a consolidated sales dataset across different retail accounts, thereby supporting accurate and consistent downstream analytics.
