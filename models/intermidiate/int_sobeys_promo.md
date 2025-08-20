# Intermediate Model: int_sobeys_promo

## Purpose
Identify promotional weeks and promo depth (% off) for Sobeys at **banner + UPC + week**.

## Inputs
- `stg_sobeys_sales`: POS fact at store level.
- `int_sobeys_stores`: store attributes with `banner` and `retail_group`.
- `calendar`: provides `week_end_date` and `week_index`.

## Method
1. **Group to banner+UPC+week**
   Weighted avg price = `SUM(dollar_sales) / NULLIF(SUM(unit_sales), 0)`.

2. **Reference price**
   Rolling max of `avg_price` over the **current and 13 prior weeks** within the same banner+UPC.

3. **Promo flag**
   Promo if `avg_price <= max_price_14w * 0.95`.

4. **% off**
   `(max_price_14w - avg_price) / max_price_14w` (null if `max_price_14w` is null/zero).

5. **Buckets**
   - `5-10%`, `10-20%`, `20%+`, else `Regular`.

## Output
- Rounds: `dollar_sales`, `avg_price`, `max_price_14w` to 2 dp; `pct_off` to 4 dp.
- Casts: `pct_off_bucket` as STRING, `is_promo_week` as BOOL.

## Incremental Strategy
Reprocess the most recent **~16 weeks** from the source sales each run to keep rolling windows correct without scanning full history.
