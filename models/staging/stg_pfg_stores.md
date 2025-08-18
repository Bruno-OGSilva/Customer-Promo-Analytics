# Staging Model: stg_pfg_stores

## Overview
The `stg_pfg_stores` model is designed to extract and transform raw PFG store data from the POS system. It sources data from the `raw_pfg_stores` table within the `pos` schema, applies column renaming, standardizes province values via a CASE statement, and creates a unique store identifier. This results in a clean, consistent dataset that is ready for downstream processing and analysis.

## Source Data
- **Source Table:** `pos.raw_pfg_stores`
- **Raw Columns:**
  - `Store Name`
  - `Store Number`
  - `Banner Name`
  - `Province Name`
  - `retail_group`

## Transformations Applied
### Column Renaming
- **Store Name → store_name:**
  The `Store Name` column is renamed to `store_name` for clarity.
- **Store Number → store_id:**
  The `Store Number` column is renamed to `store_id` and serves as the primary identifier for each store.
- **Banner Name → banner:**
  The `Banner Name` column is renamed to `banner`.
- **Province Name:**
  This column is retained; however, it is used in the transformation process to derive a standardized province code.
- **retail_group:**
  Retained as provided to indicate the grouping or affiliation of the store.

### Standardizing Province Values
A CASE statement is applied to transform full province names into their standardized two-letter abbreviations:
- When `Province Name` = 'ALBERTA' then 'AB'
- When `Province Name` = 'BRITISH COLUMBIA' then 'BC'
- When `Province Name` = 'MANITOBA' then 'MB'
- When `Province Name` = 'NEW BRUNSWICK' then 'NB'
- When `Province Name` = 'NEWFOUNDLAND AND LABRADOR' then 'NL'
- When `Province Name` = 'NORTHWEST TERRITORIES' then 'NT'
- When `Province Name` = 'NOVA SCOTIA' then 'NS'
- When `Province Name` = 'NUNAVUT' then 'NU'
- When `Province Name` = 'ONTARIO' then 'ON'
- When `Province Name` = 'PRINCE EDWARD ISLAND' then 'PE'
- When `Province Name` = 'QUEBEC' then 'QC'
- When `Province Name` = 'SASKATCHEWAN' then 'SK'
- When `Province Name` = 'YUKON' then 'YT'

The resulting value is stored in a new column named `province`.

### Derived Field
- **unique_store_id:**
  This field is derived by concatenating the `retail_group` and `Store Number` (now `store_id`) with a pipe (`|`) separator. It provides a composite unique identifier for each store, which is essential for ensuring accurate joins and aggregations in subsequent models.

## Business Logic & Rationale
- **Data Standardization:**
  Renaming fields and standardizing province codes improve the consistency and readability of the dataset, making it easier for data consumers to work with.
- **Unique Identification:**
  The `unique_store_id` ensures that each store record is uniquely identifiable, reducing the risk of duplicates or mismatches during data integration.
- **Ease of Integration:**
  With clearly defined and standardized fields, the transformed data can be reliably joined with other datasets in downstream processing and analytics.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model relies on the data provided by the `raw_pfg_stores` table in the `pos` schema. Any schema changes in the source data must be reflected in this model.
- **Testing Recommendations:**
  - **Not Null Tests:** Verify that critical fields (`store_name`, `store_id`, `banner`, `province`, and `unique_store_id`) are not null.
  - **Uniqueness Test:** Ensure that `unique_store_id` is unique across all records.
  - **Transformation Accuracy:** Confirm that the CASE statement correctly converts full province names into their corresponding two-letter abbreviations.

## Conclusion
The `stg_pfg_stores` model effectively cleans and standardizes raw store data from the POS system. By applying necessary renaming, transforming province values, and generating a unique store identifier, this model lays a solid foundation for further data processing and analysis, ensuring reliable downstream reporting and business insights.
