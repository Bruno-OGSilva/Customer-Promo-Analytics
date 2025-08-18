# Mart Model: sales

## Overview
The `sales` model consolidates sales data from multiple retail accounts into a single, unified dataset. This model is part of the mart layer and is designed to support comprehensive analysis and reporting by appending (using `UNION ALL`) the sales records from various source models. The unified dataset includes data from:

- `int_lcl_sales`
- `int_fcl_sales`
- `stg_sobeys_sales`
- `stg_ccl_sales`
- `stg_pfg_sales`
- `stg_metro_sales`

## Data Sources and Transformations
### Source Models
- **Local Sales (`lcl_sales`):**
  Derived from `int_lcl_sales`, representing sales data for the local retail account.

- **Federated Coop Sales (`fcl_sales`):**
  Derived from `int_fcl_sales`, representing sales data for Federated Coop.

- **Sobeys Sales (`sobeys_sales`):**
  Derived from `stg_sobeys_sales`, representing sales data for Sobeys.

- **CCL Sales (`ccl_sales`):**
  Derived from `stg_ccl_sales`, representing sales data for CCL.

- **PFG Sales (`pfg_sales`):**
  Derived from `stg_pfg_sales`, representing sales data for PFG.

- **Metro Sales (`metro_sales`):**
  Derived from `stg_metro_sales`, representing sales data for Metro.

### Transformation Logic
- **Appending Data:**
  Each of the source models is queried using a simple `SELECT *`, and then the records are appended together using a `UNION ALL` operation. This approach ensures that all sales records from the different retail accounts are included in the final dataset.

- **Final CTE:**
  The combined result is stored in a CTE named `sales` which is then queried using a `SELECT *` statement. This best practice helps in debugging and ensures that the final result set is clearly defined.

## Business Logic & Rationale
- **Unified View of Sales Data:**
  The purpose of the model is to create a comprehensive sales dataset that combines different retail accounts. This unified view is essential for performing cross-retail analytics and making strategic business decisions.

- **Schema Consistency:**
  Although the source models might have slight variations in their columns, only the common columns are expected to be included in the final mart layer. Any columns that are not common (like `promo_type` from FCL) are excluded in the intermediate layers to maintain consistency.

- **Facilitation of Downstream Analysis:**
  By aggregating data from multiple sources, the model simplifies further transformations, reporting, and analytics in the mart layer.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  This model depends on the successful execution and schema consistency of the following models:
  - `int_lcl_sales`
  - `int_fcl_sales`
  - `stg_sobeys_sales`
  - `stg_ccl_sales`
  - `stg_pfg_sales`
  - `stg_metro_sales`

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields across the appended datasets are not null.
  - **Schema Consistency Tests:** Confirm that common columns have matching data types and semantics across all source models.
  - **Data Quality Checks:** Validate that the union operation correctly aggregates data without introducing duplicates or inconsistencies.

## Conclusion
The `sales` mart model is a critical component for generating a holistic view of sales across various retail accounts. By unifying data from multiple source models, it provides a robust foundation for downstream business intelligence and reporting, ensuring that strategic decisions are informed by comprehensive, consolidated sales data.
