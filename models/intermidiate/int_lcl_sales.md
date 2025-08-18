# Intermediate Model: int_lcl_sales

## Overview
The `int_lcl_sales` model refines raw LCL sales data by applying necessary transformations and filtering out columns that are not common across all retail accounts. In this intermediate layer, we specifically exclude the promotional sales columns (`promo_dollar_sales` and `promo_unit_sales`) that are not present in other retail datasets. This streamlined dataset is designed to facilitate a consistent append operation in the Mart layer, where sales data from multiple retail accounts will be combined.

## Source Data
- **Source Table:** `pos.raw_lcl_sales`
- **Raw Columns:**
  - `Site Number`
  - `UPC_Description`
  - `UPC`
  - `Sales`
  - `Units`
  - `Promo Sales`
  - `Promo Units`
  - `Week End Date`
  - `retail_group`

## Transformations Applied
### Column Renaming & Data Type Casting
- **store_id:**
  Renamed from `Site Number` to clearly denote the store identifier.
- **product:**
  Derived from `UPC_Description` to represent the product name or description.
- **upc_no:**
  Retains the original `UPC` value.
- **upc_int:**
  The `UPC` value is cast to an integer to support numerical operations.
- **dollar_sales:**
  The `Sales` column is cleaned by removing currency symbols and commas, then cast to `float64` for precise financial calculations.
- **unit_sales:**
  The `Units` column is cast to `int64` to ensure consistent tracking of unit sales.
- **week_end_date:**
  The `Week End Date` column is cast to a DATE type, standardizing the format for time-series analysis.
- **retail_group:**
  Carried over from the source, representing the retail group classification.
- **unique_store_id:**
  A composite unique identifier is created by concatenating `retail_group` and `Site Number` (i.e., `store_id`) with a pipe (`|`) separator.
- **pod:**
  An additional derived field created by concatenating `retail_group`, `Site Number`, and `UPC` with pipe separators, serving as an extended unique identifier.

### Column Exclusion
- **Excluded Columns:**
  The columns `promo_dollar_sales` and `promo_unit_sales` (originally derived from `Promo Sales` and `Promo Units`) are deliberately excluded in this layer. These columns are not common to other retail accounts and are omitted to ensure consistency when appending sales data in the Mart layer.

## Business Logic & Rationale
- **Consistency Across Retail Accounts:**
  By excluding the promotional sales columns, the model produces a dataset with a consistent schema that aligns with other retail accounts. This is crucial for the final Mart layer where sales tables from different sources are combined.
- **Data Cleansing:**
  The transformation of currency fields (removing symbols and commas) and the casting of data types ensures that the numerical data is accurate and reliable for downstream analysis.
- **Unique Identification:**
  The creation of `unique_store_id` and `pod` fields helps maintain data integrity by uniquely identifying each record, which is essential for correct aggregations and joins in subsequent layers.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the data loaded into the `pos.raw_lcl_sales` table. Any changes to the source schema should be updated in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields (`store_id`, `product`, `upc_no`, `upc_int`, `dollar_sales`, `unit_sales`, `week_end_date`, `retail_group`, `unique_store_id`, and `pod`) are not null.
  - **Data Type Verification:** Confirm that numerical and date fields are cast correctly.
  - **Uniqueness Test:** Validate that `unique_store_id` is unique across records to avoid duplicates during downstream joins.

## Conclusion
The `int_lcl_sales` model provides a cleaned and standardized version of LCL sales data by removing non-essential promotional columns and ensuring consistency in data types and field naming. This intermediate layer lays a solid foundation for the Mart layer, where sales data from various retail accounts will be appended into a unified dataset for comprehensive analysis.
