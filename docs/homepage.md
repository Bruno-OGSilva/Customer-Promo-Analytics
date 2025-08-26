{% docs __overview__ %}
# DBT Project Overview: Customer Retail Analytics

This documentation provides an overview of the key models and transformations in the Customer Retail Analytics project. The project is organized into multiple layers, each serving a specific purpose in the data transformation pipeline. This overview page outlines the raw, staging, intermediate, promo-intermediate, and mart layers, along with a brief description of each model.

---

## Project Layers

### Raw Layer
- **Raw Data Ingestion:**
  Raw data is loaded directly from the source systems into tables (e.g., `pos.raw_product_mf`, `pos.raw_discount_banners`, `soft-drink-grocery.raw.raw_wno`). These tables serve as the starting point for all transformations.

### Staging Layer
- **Purpose:**
  Clean and standardize the raw data.

- **Key Models:**
  - **stg_product:**
    Extracts product data from `pos.raw_product_mf` and performs type conversions (e.g., casting UPC to integer) and cleaning.
  - **stg_sobeys_sales, stg_ccl_sales, stg_pfg_sales, stg_metro_sales, stg_fcl_sales:**
    Transform raw sales data for various retail accounts by renaming columns, converting data types, and deriving key identifiers.
  - **stg_ccl_stores, stg_fcl_stores, stg_metro_stores, stg_sobeys_stores:**
    Extract and standardize store data for each retail account.

### Intermediate Layer
- **Purpose:**
  Further refine and enrich the staging data with additional business logic.

- **Key Models:**
  - **Sales Models:**
    - **int_lcl_sales:** Refines local sales data by excluding promotional sales columns to ensure a consistent schema.
    - **int_fcl_sales:** Processes FCL sales data by removing the `promo_type` column for schema uniformity.
  - **Store Models (Channel Classification):**
    - **int_lcl_stores, int_fcl_stores, int_sobeys_stores, int_ccl_stores, int_pfg_stores, int_metro_stores:**
      Enrich store data by integrating discount banner information. A CASE statement classifies stores into "Discount" or "Conventional" channels based on whether their banner matches a list from the raw discount banners table.

### Promo-Intermediate Layer
- **Purpose:**
  Detect and measure promotional activity at the banner+UPC+week level.

- **Key Models:**
  - **int_sobeys_promo, int_ccl_promo, int_pfg_promo, int_metro_promo, int_fcl_promo, int_lcl_promo**
    - Aggregate sales to banner+UPC+week.
    - Compute weighted average price (`dollar_sales / unit_sales`).
    - Calculate the rolling 14-week max price per banner+UPC.
    - Flag a week as promo if avg_price ≤ 95% of that max.
    - Calculate % off and assign buckets: `5–10%`, `10–20%`, `20%+`, else `Regular`.
    - Rounded outputs: prices to 2 decimals, % off to 4 decimals.
    - Incremental builds refresh recent weeks using a cutoff window to maintain rolling logic.

### Mart Layer
- **Purpose:**
  Consolidate and prepare data for reporting and analysis.

- **Key Models:**
  - **sales:** Unions sales data from all retail accounts (LCL, FCL, Sobeys, CCL, PFG, Metro).
  - **stores:** Unifies store data from all intermediate store models.
  - **product:** Clean, unified product view.
  - **product_missing:** Identifies new products that have sales but are missing from the product table.
  - **calendar:** Full date dimension with retail week logic and indices.
  - **promo:** Unifies all `int_*_promo` tables into a single promo mart. Provides a retailer-agnostic fact table at the banner+UPC+week level, ready for reporting promo lift, depth, and retailer comparisons.

---

## Summary of Key Transformations

- **Data Standardization:** Columns renamed and cast consistently across staging.
- **Data Enrichment:** Store classification into Discount/Conventional channels.
- **Promo Logic:** Rolling 14-week max price, 5% threshold, % off buckets, unified in the promo mart.
- **Data Consolidation:** UNION ALL across retailers for sales, stores, and promo.
- **Calendar Dimension:** Provides consistent week-based analysis for TY vs LY, promo vs regular.

---

## Notes for Readers

- **Incremental Models:** Sales and promo-intermediate models use incremental logic with a cutoff for efficient rebuilds.
- **Retail Group Keys:** `retail_group` ensures cross-retailer joins.
- **Channel Classification:** Centralized in the intermediate store models for consistency.
- **Promo Logic Caveat:** A week is flagged as promo if avg_price ≤ 95% of the rolling 14-week max. Retailers may define promotions differently.
- **Precision:** Prices (2 dp), percent off (4 dp), buckets (`Regular`, `5-10%`, `10-20%`, `20%+`).
- **Calendar Alignment:** Week indices ensure fair comparisons across all retailers.
- **Data Freshness:** Sources monitored with 24h warn / 48h error freshness tests.

---

## Conclusion

Each model, from raw ingestion to final marts, incrementally transforms and enriches the data. This ensures downstream reporting is built on clean, consistent, and business-aligned datasets.

For detailed documentation on each model, please refer to the generated `.md` files.

{% enddocs %}
