# Intermediate Model: int_pfg_stores

## Overview
The `int_pfg_stores` model enriches PFG store data by integrating discount banner information to classify each store into a sales channel. This model builds on the base store data from the `stg_pfg_stores` staging model and utilizes discount banner information from the raw source (`pos.raw_discount_banners`). A CASE statement is used to assign a channel value of either "Discount" or "Conventional" based on whether the store's banner matches any discount banner.

## Source Data
- **PFG Stores:**
  Sourced from the `stg_pfg_stores` model, which provides core store attributes including:
  - `store_name`
  - `store_id`
  - `banner`
  - `province`
  - `retail_group`
  - `unique_store_id`

- **Discount Banners:**
  Sourced from the `pos.raw_discount_banners` table. The column `Discount Banners` is renamed to `discount_banner` to list the banners associated with discount stores.

## Transformations Applied
### Data Extraction
- **pfg_stores CTE:**
  Retrieves all records from `stg_pfg_stores` as the base dataset.

- **discount_banners CTE:**
  Extracts discount banner values from `pos.raw_discount_banners`, renaming the column to `discount_banner`.

### Channel Classification
- **pfg_stores_channel CTE:**
  The model creates a new field `channel` based on the following logic:
  - If the store's `banner` is present in the list of `discount_banner` values, then assign the channel as `'Discount'`.
  - Otherwise, assign the channel as `'Conventional'`.

  This classification is applied while selecting the relevant store attributes.

## Business Logic & Rationale
- **Channel Segmentation:**
  Differentiating between discount and conventional stores is essential for targeted analysis, reporting, and strategic decision-making. By segmenting stores based on their banner information, the model enables tailored insights into store performance.

- **Data Enrichment:**
  Integrating discount banner information enhances the base store dataset, providing an additional layer of business context that supports downstream analytics.

- **Consistency:**
  Standardizing store data with a clear channel classification ensures that the dataset can be seamlessly integrated with other data sources in later stages of the data pipeline.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - The model depends on the `stg_pfg_stores` staging model for core store data.
  - It also relies on the `pos.raw_discount_banners` source for discount banner information.

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields (`store_name`, `store_id`, `banner`, `province`, `retail_group`, `unique_store_id`, and `channel`) are not null.
  - **Channel Classification:** Validate that the `channel` field correctly categorizes stores as "Discount" when their banner is in the discount banners list and as "Conventional" otherwise.
  - **Data Integrity:** Verify that the join logic between the store data and discount banners does not lead to data loss or duplication.

## Conclusion
The `int_pfg_stores` model enriches raw PFG store data by classifying each store into a sales channel based on discount banner information. This transformation facilitates more nuanced downstream reporting and analysis by providing a clear segmentation between discount and conventional stores.
