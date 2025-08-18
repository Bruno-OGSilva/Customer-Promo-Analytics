# Mart Model: product

## Overview
The `product` mart model delivers a unified view of product information for reporting and analysis. This model serves as the final output in the product data pipeline by selecting all transformed product data from the staging layer. It ensures that downstream consumers have access to standardized and clean product details.

## Source Data
- **Staging Model:** `stg_product`
- **Key Columns:**
  - `product`
  - `upc`
  - `upc_int`
  - `vendor`
  - `brand`
  - `category`
  - `subcategory`
  - `item_size`
  - `item_unit`
  - `pack_qty`

## Transformations Applied
- **Data Extraction:**
  The model pulls all product data from the staging model `stg_product` without additional transformation. All cleaning and type conversions have been handled in the staging layer.

- **Unified Output:**
  By selecting all columns from `stg_product`, the model produces a consistent and ready-to-use dataset for further downstream analysis, reporting, and business intelligence.

## Business Logic & Rationale
- **Finalization of Product Data:**
  The mart layer represents the final step in the product data transformation process. The `product` model aggregates all the clean and standardized product details prepared in the staging layer.

- **Simplified Access for Analysis:**
  This model provides a single source of truth for product information, making it easier for analysts and decision-makers to query and generate insights without needing to join multiple sources or perform additional transformations.

- **Data Consistency:**
  Since all transformations and cleansing are completed in the staging model, the mart model ensures that the final product dataset is consistent and reliable for downstream reporting.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model depends on the successful execution of the `stg_product` model. Any changes to the product data in the staging layer must be reflected in this mart model.

- **Testing Recommendations:**
  - **Not Null Tests:** Ensure that key fields (e.g., `product`, `upc`, `upc_int`) are not null.
  - **Data Consistency Tests:** Verify that the final dataset maintains the expected schema and that all columns are correctly populated from the staging layer.
  - **Uniqueness Tests:** If applicable, validate that unique identifiers (if any) remain consistent in the final output.

## Conclusion
The `product` mart model serves as the final, unified view of product information within the data pipeline. By directly selecting data from the well-transformed staging layer, it provides a clean, consistent, and easily accessible dataset for comprehensive product reporting and analysis.
