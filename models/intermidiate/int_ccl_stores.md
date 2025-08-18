# Intermediate Model: int_ccl_stores

## Overview
The `int_ccl_stores` model enriches CCL store data by integrating discount banner information to classify each store into a sales channel. This intermediate layer builds on the raw store data from the staging model (`stg_ccl_stores`) and uses discount banner data from the `pos.raw_discount_banners` source to determine whether a store is part of the "Discount" or "Conventional" channel. This classification is essential for downstream analysis and reporting.

## Source Data
- **CCL Stores:**
  Sourced from the `stg_ccl_stores` model. This dataset includes key store attributes such as:
  - `store_name`
  - `store_id`
  - `banner`
  - `province`
  - `retail_group`
  - `unique_store_id`

- **Discount Banners:**
  Sourced from the `pos.raw_discount_banners` table. The column `Discount Banners` is renamed to `discount_banner` in this model, and it lists the banners that are associated with discount stores.

## Transformations Applied
### Data Selection
- **ccl_stores CTE:**
  Retrieves all records from the staging model `stg_ccl_stores` containing the core store data.

- **discount_banners CTE:**
  Extracts the discount banner values from the raw discount banners source, renaming the column to `discount_banner`.

### Channel Classification
- **ccl_stores_channel CTE:**
  This step combines the store data with discount banner information by:
  - Retaining key store attributes (`store_name`, `store_id`, `banner`, `province`, `retail_group`, and `unique_store_id`).
  - Creating a new field, `channel`, using a CASE statement:
    - If the store's `banner` is found in the list of `discount_banner` values, the store is classified as `'Discount'`.
    - Otherwise, the store is classified as `'Conventional'`.

## Business Logic & Rationale
- **Channel Segmentation:**
  Differentiating stores as "Discount" or "Conventional" allows for more precise analysis and targeted business strategies. This segmentation is based on the store's banner, which is matched against a predefined list of discount banners.

- **Data Enrichment:**
  By integrating discount banner data, the model adds an important layer of business context to the store information, which supports downstream analytical processes and decision making.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - The model relies on the `stg_ccl_stores` staging model for the base store data.
  - It also depends on the `pos.raw_discount_banners` source for discount banner information.

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields (`store_name`, `store_id`, `banner`, `province`, `retail_group`, `unique_store_id`, and `channel`) are not null.
  - **Channel Classification:** Verify that the `channel` field correctly categorizes stores as "Discount" or "Conventional" based on the banner values.
  - **Data Integrity:** Ensure that the join and filtering logic between the store data and discount banners does not result in unexpected data loss or duplication.

## Conclusion
The `int_ccl_stores` model enriches the CCL store data by adding a sales channel classification derived from discount banner information. This transformation is crucial for enabling targeted downstream analyses and ensuring that stores are appropriately segmented in the final reporting layer.
