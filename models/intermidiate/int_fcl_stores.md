# Intermediate Model: int_fcl_stores

## Overview
The `int_fcl_stores` model enriches the Federated Coop (FCL) store data by integrating discount information to segment stores into different sales channels. This model builds upon the staging layer by joining store details with discount banner data to classify each store as either "Discount" or "Conventional". This classification is crucial for downstream analysis, as it allows for targeted reporting and strategy formulation based on the sales channel.

## Source Data
- **FCL Stores:**
  Sourced from the staging model `stg_fcl_stores`, which provides detailed store information such as store name, store ID, banner, province, retail group, and a composite unique store identifier.

- **Discount Banners:**
  Sourced from the raw table `pos.raw_discount_banners`. This table contains the list of banners that are associated with discount stores. The column `Discount Banners` is renamed to `discount_banner` in this model.

## Transformations Applied
### Data Selection and Integration
- **FCL Stores Data:**
  The model first retrieves all records from `stg_fcl_stores` into the CTE `fcl_stores`.

- **Discount Banners Data:**
  The model retrieves the discount banner values from the `raw_discount_banners` table into the CTE `discount_banners`.

### Channel Classification
- **Channel Determination:**
  In the `fcl_stores_channel` CTE, a new field named `channel` is created based on the value of the `banner` field:
  - If the store's `banner` matches any value from the `discount_banners`, the store is classified as `'Discount'`.
  - Otherwise, it is classified as `'Conventional'`.

### Derived Output
- The final output of the model consists of:
  - Standard store attributes: `store_name`, `store_id`, `banner`, `province`, `retail_group`, and `unique_store_id`.
  - A derived `channel` field that indicates whether a store belongs to the "Discount" or "Conventional" channel.

## Business Logic & Rationale
- **Channel Segmentation:**
  Differentiating between discount and conventional stores is critical for performance analysis, marketing strategy, and inventory management. By classifying stores based on their banner information, stakeholders can more easily analyze trends and make informed decisions.

- **Data Enrichment:**
  The integration of discount banner information enriches the base store data, adding a layer of segmentation that is not present in the raw data. This is especially valuable when consolidating data for unified reporting.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - The model depends on the `stg_fcl_stores` staging model for the base store data.
  - It also relies on the `pos.raw_discount_banners` source for discount banner values.

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields such as `store_name`, `store_id`, `banner`, and `channel` are not null.
  - **Channel Classification:** Validate that the `channel` field correctly categorizes stores by comparing the `banner` values against the list in `discount_banners`.
  - **Data Integrity:** Verify that the join between `fcl_stores` and `discount_banners` is correctly implemented, ensuring no unintended data loss or duplication.

## Conclusion
The `int_fcl_stores` model is an essential intermediate layer that adds valuable business context by classifying Federated Coop stores into discount and conventional channels. This enrichment supports more granular analysis and enables better-informed strategic decisions in the downstream Mart layer.
