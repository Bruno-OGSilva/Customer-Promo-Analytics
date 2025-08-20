{{ config(
  materialized        = 'incremental',
  unique_key          = ['retail_group','banner','upc_no','week_index'],
  partition_by        = {'field': 'week_end_date', 'data_type': 'date'},
  cluster_by          = ['retail_group','banner','upc_no'],
  on_schema_change    = 'sync_all_columns'
) }}

-- Reprocess a rolling window each incremental run so pct_off windows stay correct
with cutoff as (
  select date_sub(max(week_end_date), interval 16 week) as cutoff_date
  from {{ ref('calendar') }}
),

ccl as (
  select
    retail_group, banner, upc_no, product, week_end_date, week_index,
    dollar_sales, unit_sales, avg_price, max_price_14w, pct_off, pct_off_bucket, is_promo_week
  from {{ ref('int_ccl_promo') }}
  {% if is_incremental() %}
    where week_end_date >= (select cutoff_date from cutoff)
  {% endif %}
),

fcl as (
  select
    retail_group, banner, upc_no, product, week_end_date, week_index,
    dollar_sales, unit_sales, avg_price, max_price_14w, pct_off, pct_off_bucket, is_promo_week
  from {{ ref('int_fcl_promo') }}
  {% if is_incremental() %}
    where week_end_date >= (select cutoff_date from cutoff)
  {% endif %}
),

lcl as (
  select
    retail_group, banner, upc_no, product, week_end_date, week_index,
    dollar_sales, unit_sales, avg_price, max_price_14w, pct_off, pct_off_bucket, is_promo_week
  from {{ ref('int_lcl_promo') }}
  {% if is_incremental() %}
    where week_end_date >= (select cutoff_date from cutoff)
  {% endif %}
),

metro as (
  select
    retail_group, banner, upc_no, product, week_end_date, week_index,
    dollar_sales, unit_sales, avg_price, max_price_14w, pct_off, pct_off_bucket, is_promo_week
  from {{ ref('int_metro_promo') }}
  {% if is_incremental() %}
    where week_end_date >= (select cutoff_date from cutoff)
  {% endif %}
),

pfg as (
  select
    retail_group, banner, upc_no, product, week_end_date, week_index,
    dollar_sales, unit_sales, avg_price, max_price_14w, pct_off, pct_off_bucket, is_promo_week
  from {{ ref('int_pfg_promo') }}
  {% if is_incremental() %}
    where week_end_date >= (select cutoff_date from cutoff)
  {% endif %}
),

sobeys as (
  select
    retail_group, banner, upc_no, product, week_end_date, week_index,
    dollar_sales, unit_sales, avg_price, max_price_14w, pct_off, pct_off_bucket, is_promo_week
  from {{ ref('int_sobeys_promo') }}
  {% if is_incremental() %}
    where week_end_date >= (select cutoff_date from cutoff)
  {% endif %}
)

select * from ccl
union all
select * from fcl
union all
select * from lcl
union all
select * from metro
union all
select * from pfg
union all
select * from sobeys
