# Mart: promo

## What it is
A unified promotions mart combining all retailer-specific intermediate promo tables:
- `int_ccl_promo`, `int_fcl_promo`, `int_lcl_promo`,
- `int_metro_promo`, `int_pfg_promo`, `int_sobeys_promo`.

Grain: **banner + UPC + week**.

## How it’s built
- Unions all intermediate models, which already compute:
  - weighted `avg_price` = SUM(dollar_sales) / SUM(unit_sales),
  - rolling 14-week `max_price_14w`,
  - `% off` vs the rolling max,
  - `pct_off_bucket` and `is_promo_week`.
- Incremental refresh reprocesses the most recent ~16 weeks (via `calendar`) so rolling windows remain correct.

## Why it’s useful
Gives a single, comparable view of promo intensity and timing across banners and retailers, ready for category readouts, lift analyses, and promo depth segmentation.
