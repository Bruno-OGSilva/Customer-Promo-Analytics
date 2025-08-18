# Intermediate Model: int_metro_stores

## Overview
The `int_metro_stores` model enhances Metro store data by adding a sales channel classification based on discount banner information. This model builds upon the base store data from the staging model (`stg_metro_stores`) and uses discount banner data from the raw source (`pos.raw_discount_banners`) to determine whether each store should be classified as "Discount" or "Conventional." This classification enables more targeted downstream analysis and reporting.

## Source Data
- **Metro Stores:**
  Sourced from the `stg_metro_stores` model, which includes key store attributes such as:
  - `store_name`
  - `store_id`
  - `banner`
  - `province`
  - `retail_group`
  - `unique_store_id`

- **Discount Banners:**
  Sourced from the `pos.raw_discount_banners` table. The column `Discount Banners` is renamed to `discount_banner` and provides a list of banners associated with discount stores.

## Transformations Applied
### Data Extraction and Selection
- **metro_stores CTE:**
  Retrieves all records from the `stg_metro_stores` model to serve as the base dataset for Metro store information.

- **discount_banners CTE:**
  Extracts discount banner values from the `pos.raw_discount_banners` source, renaming the column to `discount_banner`.

### Channel Classification
- **metro_stores_channel CTE:**
  The model applies a CASE statement to determine the sales channel for each store:
  - **Discount:**
    If the store’s `banner` is found within the list of discount banners.
  - **Conventional:**
    If the store’s `banner` does not match any value in the discount banners list.

  This classification is added as a new field, `channel`, along with the original store attributes.

## Business Logic & Rationale
- **Channel Segmentation:**
  Classifying stores as "Discount" or "Conventional" is essential for segmenting performance metrics, tailoring marketing strategies, and optimizing inventory management.

- **Data Enrichment:**
  By incorporating discount banner data, the model enriches the store dataset with a meaningful business attribute that supports more granular analysis.

- **Consistency:**
  Standardizing the classification across all Metro stores ensures that downstream models and reports operate on a uniform schema, facilitating accurate comparisons and aggregations.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - The model relies on the `stg_metro_stores` staging model for the base Metro store data.
  - It also depends on the `pos.raw_discount_banners` source for the discount banner values.

- **Testing Recommendations:**
  - **Not Null Tests:**
    Ensure that critical fields (`store_name`, `store_id`, `banner`, `province`, `retail_group`, `unique_store_id`, and `channel`) are not null.
  - **Channel Classification Verification:**
    Validate that the `channel` field correctly classifies stores based on the presence or absence of discount banners.
  - **Data Integrity:**
    Confirm that the join and filtering logic between the Metro store data and discount banners does not result in data loss or duplication.

## Conclusion
The `int_metro_stores` model successfully enriches the Metro store dataset by incorporating discount banner information to classify each store as either "Discount" or "Conventional." This added layer of classification supports more targeted analysis in downstream reporting and business intelligence efforts.
