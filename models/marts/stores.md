# Mart Model: stores

## Overview
The `stores` model consolidates store data from multiple retail accounts into a single, unified dataset. This model is part of the mart layer and serves as the final source of store information that can be used for reporting and analysis across various retail channels.

## Data Sources and Transformations
### Source Models
This model unions data from the following intermediate models:
- **Local Stores:** `int_lcl_stores`
- **Federated Coop Stores:** `int_fcl_stores`
- **Sobeys Stores:** `int_sobeys_stores`
- **CCL Stores:** `int_ccl_stores`
- **PFG Stores:** `int_pfg_stores`
- **Metro Stores:** `int_metro_stores`

### Transformation Logic
- **Union Operation:**
  The model uses `UNION ALL` to append rows from each of the source models. This ensures that all store records from different retail accounts are included in the final dataset.

- **Column Consistency:**
  The union is performed on the assumption that the source models share a common schema. Common columns typically include:
  - `store_name`
  - `store_id`
  - `banner`
  - `province`
  - `retail_group`
  - `unique_store_id`
  - `channel`

  This consistency is critical to allow the union operation without schema conflicts.

## Business Logic & Rationale
- **Unified View of Stores:**
  Combining store data from multiple retail accounts provides a single point of reference for store-level analysis. This unified view supports cross-channel performance comparisons, trend analysis, and strategic decision-making.

- **Consistency Across Channels:**
  By ensuring a consistent set of columns across all intermediate models, the unioned dataset provides a reliable basis for downstream analytics in the mart layer.

- **Simplified Reporting:**
  The consolidated dataset eliminates the need to query multiple sources individually, simplifying reporting and analysis across different retail accounts.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  This model depends on the successful execution of the following intermediate models:
  - `int_lcl_stores`
  - `int_fcl_stores`
  - `int_sobeys_stores`
  - `int_ccl_stores`
  - `int_pfg_stores`
  - `int_metro_stores`

- **Testing Recommendations:**
  - **Not Null Tests:** Verify that key fields (e.g., `store_id`, `store_name`, `unique_store_id`, and `channel`) are not null in the final unioned dataset.
  - **Uniqueness Tests:** Ensure that the composite key (`unique_store_id`) maintains its uniqueness across the unioned records.
  - **Schema Consistency:** Validate that the schema is consistent across
