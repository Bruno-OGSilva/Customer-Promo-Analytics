# Staging Model: stg_sobeys_stores

## Overview
The `stg_sobeys_stores` model is designed to extract and transform raw store data for Sobeys from the POS system. It pulls data from the `raw_sobeys_stores` source in the `pos` schema, standardizes column names, and derives a unique store identifier. This cleaned data serves as the foundation for downstream analytics and reporting in your data warehouse.

## Source Data
- **Source Table:** `pos.raw_sobeys_stores`
- **Raw Columns:**
  - `Geography`
  - `Store No`
  - `Division Name`
  - `Format Name`
  - `Banners Name`
  - `Province Name`
  - `retail_group`

## Transformations Applied
### Renaming Columns
- **Geography → store_name:** Represents the store's name or location.
- **Store No → store_id:** A unique identifier for each store.
- **Division Name → division:** Indicates the operational division of the store.
- **Format Name → format:** Denotes the store format.
- **Banners Name → banner:** Represents the banner under which the store operates.
- **Province Name → province:** Specifies the province where the store is located.
- **retail_group:** Retained as-is to indicate the retail group classification.

### Derived Field
- **unique_store_id:**
  Created by concatenating `retail_group` and `Store No` with a pipe (`|`) separator. This composite key ensures each store is uniquely identified across the dataset, facilitating reliable joins and aggregations in later transformations.

## Business Logic & Rationale
- **Standardization:** Renaming columns improves clarity, making it easier for data analysts to understand and use the data.
- **Unique Identification:** The `unique_store_id` field is critical for merging store data with other datasets, ensuring that every store can be uniquely identified.
- **Data Integrity:** Minimal transformations ensure that the original data is preserved while being made more accessible for subsequent processing.

## Dependencies & Testing Considerations
- **Source Dependency:** This model relies on the `raw_sobeys_stores` table in the `pos` schema. Any changes to the source schema should be promptly reflected in this model.
- **Quality Checks:** Consider implementing dbt tests to validate:
  - Non-null values for critical fields such as `store_name`, `store_id`, and `unique_store_id`.
  - Uniqueness of `unique_store_id` to prevent duplicate store records.

## Conclusion
The `stg_sobeys_stores` model is a crucial component of your data pipeline. By standardizing and enhancing the raw store data, this model lays a strong foundation for accurate, efficient downstream analyses in your data warehouse environment.
