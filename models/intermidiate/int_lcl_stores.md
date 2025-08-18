# Intermediate Model: int_lcl_stores

## Overview
The `int_lcl_stores` model enriches local (LCL) store data by integrating discount banner information to classify each store into a sales channel. This intermediate layer builds on the staging model (`stg_lcl_stores`) and leverages discount banner data from the raw source to determine whether a store is categorized as "Discount" or "Conventional." This classification is critical for downstream reporting and analysis.

## Source Data
- **LCL Stores:**
  Sourced from the `stg_lcl_stores` model, which provides core store information including:
  - `store_name`
  - `store_id`
  - `banner`
  - `province`
  - `retail_group`
  - `unique_store_id`

- **Discount Banners:**
  Sourced from the `pos.raw_discount_banners` table. This table contains a list of discount banners under the column `Discount Banners`, which is renamed to `discount_banner` in this model.

## Transformations Applied
### Data Selection
- **lcl_stores CTE:**
  Retrieves all records from `stg_lcl_stores` to serve as the base dataset for local stores.

- **discount_banners CTE:**
  Extracts the discount banner values from the raw discount banners source, renaming the column to `discount_banner`.

### Channel Classification
- **lcl_stores_channel CTE:**
  In this step, the model:
  - Selects the key store attributes: `store_name`, `store_id`, `banner`, `province`, `retail_group`, and `unique_store_id`.
  - Creates a new field called `channel` using a CASE statement:
    - If the store's `banner` exists in the list of discount banners, it is classified as `'Discount'`.
    - Otherwise, it is classified as `'Conventional'`.

## Business Logic & Rationale
- **Channel Segmentation:**
  Classifying stores into "Discount" or "Conventional" channels provides valuable insights into store operations and helps tailor marketing strategies and inventory management.

- **Data Enrichment:**
  The integration of discount banner information enriches the local store data by adding a meaningful classification, which is useful for further analysis in downstream processes.

- **Consistency:**
  Standardizing the store data by assigning a channel ensures that downstream models and reporting layers work with a unified schema, making it easier to compare performance across different store segments.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - This model relies on the `stg_lcl_stores` staging model for the core local store data.
  - It also depends on the `pos.raw_discount_banners` source for the discount banner values.

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields such as `store_name`, `store_id`, `banner`, `province`, `retail_group`, `unique_store_id`, and `channel` are not null.
  - **Channel Classification Test:** Validate that the `channel` field correctly categorizes stores as "Discount" when their banner is in the discount banners list, and as "Conventional" otherwise.
  - **Data Integrity:** Confirm that the join between the store data and discount banners does not introduce duplicates or drop records unintentionally.

## Conclusion
The `int_lcl_stores` model enhances local store data by appending a sales channel classification based on discount banner information. This transformation lays a robust foundation for subsequent reporting and analytics, ensuring that store performance can be accurately segmented and analyzed.
