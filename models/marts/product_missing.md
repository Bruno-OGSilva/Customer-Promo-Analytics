# Mart Model: product_missing

## Overview
The `product_missing` model is designed to identify new product items that have recorded sales but are missing from the product dimension. This model serves as a diagnostic tool to alert data stewards about products that need to be manually added to the product table. By highlighting discrepancies between the sales data and the product reference data, the model ensures that the product dimension remains current and complete.

## Source Data
- **Product Data:**
  Sourced from the staging model `stg_product`, which contains all currently registered products.

- **Sales Data:**
  Sourced from the consolidated `sales` mart model, which aggregates sales records from various retail accounts.

## Transformations Applied
- **Left Join:**
  The model performs a left join between the sales data (alias `a`) and the product data (alias `b`) on the UPC field:
  - `a.upc_no` from the sales records is joined with `b.upc` from the product table.

- **Filtering for Missing Products:**
  The join is filtered to include only those sales records for which no corresponding product exists in the product table (i.e., where `b.brand` is NULL).

- **Column Selection:**
  The final output selects:
  - `a.product` – the product name from sales data.
  - `a.upc_no` – the UPC from sales.
  - `a.retail_group` – the retail group classification from sales.
  - `b.brand` – expected to be NULL for missing products, which confirms the absence of the product in the reference table.

## Business Logic & Rationale
- **Identify Gaps:**
  This model flags any new products that are actively selling but have not yet been incorporated into the product dimension.
- **Manual Update Trigger:**
  By listing these missing products, the model acts as a trigger for data stewards to manually update and enrich the product table.
- **Quality Assurance:**
  Maintaining an up-to-date product dimension is crucial for accurate reporting and downstream analytics. This model provides a systematic way to catch discrepancies.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - The model depends on the `stg_product` model for the current list of registered products.
  - It relies on the `sales` model for actual sales records.

- **Testing Recommendations:**
  - **Join Accuracy:** Validate that the join condition correctly matches the UPC values from both sources.
  - **Null Checks:** Confirm that the resulting `brand` field is NULL for products missing from the product table.
  - **Data Completeness:** Ensure that the list of missing products accurately reflects new items present in the sales data.

## Conclusion
The `Product_missing` model provides a vital checkpoint in the data pipeline by ensuring that any new products evidenced in sales data are flagged for manual review and addition to the product dimension. This proactive approach helps maintain the accuracy and completeness of product information across the organization.
