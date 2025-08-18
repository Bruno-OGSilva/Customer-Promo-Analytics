# Staging Model: stg_lcl_stores

## Overview
The `stg_lcl_stores` model extracts, cleans, and transforms raw store data from the POS system for LCL. It sources data from the `raw_lcl_stores` table within the `pos` schema, renames key columns to more descriptive names, applies standardization logic to the `banner` column, and derives a composite unique identifier. These transformations ensure that the data is standardized and ready for downstream analytical processing.

## Source Data
- **Source Table:** `pos.raw_lcl_stores`
- **Raw Columns:**
  - `Store Name`
  - `Store No`
  - `Division`
  - `Store Banner`
  - `Prv`
  - `retail_group`

## Transformations Applied
### Column Renaming
- **Store Name → store_name:**
  The `Store Name` column is renamed to `store_name` to clearly indicate the store's name.
- **Store No → store_id:**
  The `Store No` column is renamed to `store_id`, serving as the primary identifier for each store.
- **Division → division:**
  The `Division` field is retained and renamed to `division` to represent the operational division of the store.
- **Store Banner → banner:**
  The `Store Banner` column is renamed to `banner` to denote the store's banner or brand.
- **Prv → province:**
  The `Prv` column is renamed to `province` to standardize the representation of province information.
- **retail_group:**
  This field is carried over unchanged from the source data.

### Data Standardization
- **Banner Standardization:**
  The `banner` column is standardized to ensure consistency:
  - Variations of "NoFrills" (e.g., "nofrills", "Nofrills") are standardized as **"NoFrills"**.
  - "no name store" is standardized as **"no name"**.
  - All other values remain unchanged.

### Derived Field
- **unique_store_id:**
  A composite unique identifier is created by concatenating `retail_group` and `Store No` (now `store_id`) with a pipe (`|`) separator. This unique key ensures each store record can be reliably joined and aggregated in downstream processes.

## Business Logic & Rationale
- **Data Standardization:**
  Renaming columns to standardized names and ensuring consistent values for the `banner` column improves data clarity and consistency across the dataset.
- **Unique Identification:**
  The creation of `unique_store_id` is critical for accurately identifying each store, reducing duplication, and enabling reliable data joins.
- **Foundation for Downstream Processing:**
  By transforming and standardizing the raw data, the model lays a robust foundation for further analytical modeling and business intelligence activities.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the data provided by the `raw_lcl_stores` table in the `pos` schema. Any modifications to the source schema should be reflected in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields such as `store_name`, `store_id`, `division`, `banner`, `province`, and `unique_store_id` are not null.
  - **Uniqueness Test:** Verify that the `unique_store_id` is unique across all records to prevent duplicate entries.
  - **Transformation Accuracy:** Validate that the renaming, standardization, and concatenation operations are correctly applied.

## Conclusion
The `stg_lcl_stores` model standardizes raw store data by renaming columns, applying banner standardization, and generating a unique store identifier. This transformation ensures that the dataset is consistent, reliable, and ready for integration into downstream analytical workflows.
