# Staging Model: stg_ccl_stores

## Overview
The `stg_ccl_stores` model is designed to extract, transform, and standardize raw store data for CCL from the POS system. Data is sourced from the `raw_ccl_stores` table in the `pos` schema. This model renames key columns, assigns a hard-coded province value, and derives a unique store identifier to support reliable joins and downstream analysis.

## Source Data
- **Source Table:** `pos.raw_ccl_stores`
- **Raw Columns:**
  - `Geography`
  - `Store Number`
  - `Division Name`
  - `retail_group`

## Transformations Applied
### Renaming Columns
- **Geography → store_name:**
  The original `Geography` column is repurposed to represent the store's name.
- **Store Number → store_id:**
  Renamed to clearly indicate the unique identifier for each store.
- **Division Name → banner:**
  The `Division Name` field is repurposed to denote the store's banner.
- **Hardcoded Province:**
  A new column `province` is introduced and set to `'AB'` to indicate the province.
- **retail_group:**
  This field is carried forward as provided in the raw data.

### Derived Field
- **unique_store_id:**
  Constructed by concatenating `retail_group` and `Store Number` with a pipe (`|`) separator. This composite key ensures that each store can be uniquely identified, simplifying joins and aggregations in later stages.

## Business Logic & Rationale
- **Data Standardization:**
  By renaming and standardizing column names, the model improves clarity and consistency across the dataset.
- **Hardcoded Province Value:**
  The model assigns a constant province value (`'AB'`) to ensure that all records are uniformly tagged, particularly useful when the source does not provide this detail.
- **Unique Identification:**
  The creation of the `unique_store_id` is vital for linking store data with other datasets, ensuring that each store record is distinct and eliminating potential duplicates.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the successful ingestion of raw data from the `pos.raw_ccl_stores` table. Any changes to the raw schema should be reflected in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Verify that essential fields such as `store_name`, `store_id`, and `unique_store_id` are not null.
  - **Uniqueness Test:** Ensure that the `unique_store_id` is unique across all records.
  - **Consistency Check:** Confirm that the hardcoded `province` field consistently holds the value `'AB'`.

## Conclusion
The `stg_ccl_stores` model lays the groundwork for reliable downstream processing by standardizing raw store data from CCL. With clear naming conventions, proper field derivation, and consistent tagging, this model ensures that the data is clean, unique, and ready for further transformation and analysis.
