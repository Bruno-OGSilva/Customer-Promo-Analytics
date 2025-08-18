# Staging Model: stg_fcl_stores

## Overview
The `stg_fcl_stores` model extracts and transforms store data for Federated Coop from the raw FCL sales dataset. It pulls data from the `pos.raw_fcl_sales` table, applies column renaming, assigns a constant banner value, and generates a composite unique identifier. These transformations standardize the data for reliable downstream processing and analysis.

## Source Data
- **Source Table:** `pos.raw_fcl_sales`
- **Raw Columns:**
  - `Store Name`
  - `Store Number`
  - `Province`
  - `retail_group`

## Transformations Applied
### Column Renaming
- **`Store Name` → store_name:**
  Renamed to clearly represent the name of the store.
- **`Store Number` → store_id:**
  Renamed to serve as the unique identifier for each store.
- **Banner Field:**
  A constant value `'Federated Coop'` is assigned to the banner field.
- **Province:**
  The `Province` column is retained to indicate the geographical location of the store.
- **retail_group:**
  Carried over from the source data for further classification.

### Derived Field
- **unique_store_id:**
  This field is created by concatenating `retail_group` and `Store Number` with a pipe (`|`) separator. It serves as a composite unique identifier, ensuring each store record is uniquely identifiable for joins and aggregations.

## Business Logic & Rationale
- **Standardization:**
  By renaming columns and standardizing field values, the model enhances clarity and consistency across the dataset.
- **Constant Banner Value:**
  Assigning a fixed banner value of `'Federated Coop'` clearly categorizes the stores within this dataset.
- **Unique Identification:**
  The `unique_store_id` is essential for ensuring that each store can be uniquely joined with other datasets, reducing the risk of duplicates in downstream analysis.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the structure and integrity of the `pos.raw_fcl_sales` table. Any changes in the source schema should be reflected in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that fields such as `store_name`, `store_id`, `banner`, `province`, and `unique_store_id` are not null.
  - **Uniqueness Test:** Verify that `unique_store_id` is unique across all records.

## Conclusion
The `stg_fcl_stores` model effectively cleans and standardizes raw Federated Coop store data, setting a robust foundation for downstream reporting and analytics. Its transformations ensure that the data is accurate, consistent, and uniquely identifiable, supporting reliable integration into broader analytical workflows.
