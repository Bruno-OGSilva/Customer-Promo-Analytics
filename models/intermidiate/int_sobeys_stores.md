# Intermediate Model: int_sobeys_stores

## Overview
The `int_sobeys_stores` model enhances Sobeys store data by incorporating discount banner information to classify each store into a sales channel. This intermediate layer builds on the base store data from the staging model (`stg_sobeys_stores`) and uses discount banner data from the raw source (`pos.raw_discount_banners`) to determine whether each store should be categorized as "Discount" or "Conventional." This classification supports more targeted analysis and reporting in downstream layers.

## Source Data
- **Sobeys Stores:**
  Sourced from the `stg_sobeys_stores` model, which provides core store attributes, including:
  - `store_name`
  - `store_id`
  - `banner`
  - `province`
  - `retail_group`
  - `unique_store_id`

- **Discount Banners:**
  Sourced from the `pos.raw_discount_banners` table. This table includes a column named `Discount Banners` which is renamed to `discount_banner` in this model, and contains the list of banners that are considered discount.

## Transformations Applied
### Data Extraction
- **sobeys_stores CTE:**
  Retrieves all records from the `stg_sobeys_stores` model as the base dataset for Sobeys stores.

- **discount_banners CTE:**
  Extracts discount banner values from `pos.raw_discount_banners` and renames the column to `discount_banner`.

### Channel Classification
- **sobeys_stores_channel CTE:**
  This step performs the following:
  - Selects key attributes from the Sobeys store data (`store_name`, `store_id`, `banner`, `province`, `retail_group`, and `unique_store_id`).
  - Introduces a new field, `channel`, using a CASE statement:
    - If the store's `banner` matches any value in the `discount_banner` list, then `channel` is set to `'Discount'`.
    - Otherwise, `channel` is set to `'Conventional'`.

## Business Logic & Rationale
- **Channel Segmentation:**
  Differentiating between discount and conventional stores is vital for targeted performance analysis and tailored strategic decisions.

- **Data Enrichment:**
  Integrating discount banner data enriches the store information, allowing for more nuanced segmentation and analysis in downstream reporting.

- **Consistency:**
  By classifying each store based on its banner, the model ensures a consistent dataset that aligns with the requirements for further aggregation and cross-retail comparison.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - This model depends on the `stg_sobeys_stores` staging model for base Sobeys store data.
  - It also depends on the `pos.raw_discount_banners` source for discount banner values.

- **Testing Recommendations:**
  - **Not Null Tests:**
    Validate that essential fields such as `store_name`, `store_id`, `banner`, `province`, `retail_group`, `unique_store_id`, and `channel` are not null.
  - **Channel Classification Validation:**
    Ensure that the `channel` field correctly classifies stores as "Discount" when the banner is present in the discount banners list and "Conventional" otherwise.
  - **Data Integrity:**
    Confirm that the join and filtering logic between the store data and discount banners does not lead to data loss or duplicate records.

## Conclusion
The `int_sobeys_stores` model effectively enriches Sobeys store data by applying a discount-based channel classification. This additional layer of segmentation facilitates more targeted analysis and reporting in subsequent data mart layers, ensuring that business insights are derived from a well-structured and consistent dataset.
