# Staging Model: stg_product

## Overview
The `stg_product` model is responsible for extracting and transforming raw product data from the POS system. It reads data from the `raw_product_mf` source and prepares it for further analysis by selecting key product attributes and performing necessary type conversions. This staging layer ensures that the product data is clean, consistent, and ready for downstream processing.

## Source Data
- **Source Table:** `pos.raw_product_mf`
- **Raw Columns:**
  - `product`
  - `upc`
  - `vendor`
  - `brand`
  - `category`
  - `subcategory`
  - `item_size`
  - `item_unit`
  - `pack_qty`

## Transformations Applied
### Column Selection and Data Type Casting
- **product:**
  Retains the product name or identifier as provided in the raw data.

- **upc and upc_int:**
  - The `upc` column is selected as-is to maintain the original UPC value.
  - A new field, `upc_int`, is created by casting the `upc` value to an integer. This enables numerical operations and comparisons where needed.

- **vendor, brand, category, subcategory, item_size, item_unit, pack_qty:**
  These fields are selected directly from the source without additional transformation, ensuring that key product attributes are preserved.

## Business Logic & Rationale
- **Data Consistency:**
  Casting the `upc` to an integer in the `upc_int` field standardizes the UPC format for downstream processes and analytics.

- **Preparation for Analysis:**
  By extracting and transforming only the essential product attributes, this model lays a robust foundation for further enrichment and integration in subsequent layers of the data pipeline.

- **Simplified Data Structure:**
  The model filters out any unnecessary fields, focusing on the most relevant product details, which simplifies downstream data transformations and reporting.

## Dependencies & Testing Considerations
- **Source Dependency:**
  This model relies on the `pos.raw_product_mf` source table. Any changes to the raw product data schema must be reflected in this staging model.

- **Testing Recommendations:**
  - **Not Null Tests:** Verify that critical fields such as `product`, `upc`, and `upc_int` are not null.
  - **Data Type Verification:** Ensure that the casting of `upc` to `upc_int` is correctly performed and that the data type conversion is consistent.
  - **Uniqueness/Consistency:** Validate that the product records remain consistent after transformation, preserving key identifiers for downstream use.

## Conclusion
The `stg_product` model effectively transforms raw product data into a clean and consistent format by selecting essential attributes and performing necessary type conversions. This standardization is crucial for ensuring reliable downstream processing, accurate analysis, and efficient reporting.
