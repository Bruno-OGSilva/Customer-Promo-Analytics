{{ config(
  materialized = 'incremental',
  unique_key   = ['banner','upc_no','week_index'],
  partition_by = {field: 'week_end_date', data_type: 'date'},
  cluster_by   = ['banner','upc_no'],
  on_schema_change = 'sync_all_columns'
) }}

with sales as (  -- source: stg_sobeys_sales
  select
    a.upc_no,
    a.product,
    a.week_end_date,
    a.dollar_sales,
    a.unit_sales,
    a.unique_store_id
  from {{ ref('stg_sobeys_sales') }} a
  {% if is_incremental() %}
    where a.week_end_date >= (
      select date_sub(max(week_end_date), interval 16 week)
      from {{ this }}
    )
  {% endif %}
),

stores as (  -- source: int_sobeys_stores
  select
    b.unique_store_id,
    b.banner,
    b.retail_group
  from {{ ref('int_sobeys_stores') }} b
),

cal as (  -- source: calendar
  select
    c.week_end_date,
    c.week_index
  from {{ ref('calendar') }} c
),

agg as (  -- banner + upc + week, weighted price
  select
    t.banner,
    t.retail_group,
    s.upc_no,
    any_value(s.product) as product,
    s.week_end_date,
    u.week_index,
    sum(s.dollar_sales) as revenue,
    sum(s.unit_sales)   as units,
    safe_divide(sum(s.dollar_sales), nullif(sum(s.unit_sales), 0)) as avg_price
  from sales s
  join stores t on s.unique_store_id = t.unique_store_id
  join cal    u on s.week_end_date   = u.week_end_date
  group by 1,2,3,5,6
),

ref as (  -- rolling 14-week max price
  select
    banner,
    retail_group,
    upc_no,
    product,
    week_end_date,
    week_index,
    revenue,
    units,
    avg_price,
    max(avg_price) over (
      partition by banner, upc_no
      order by week_index
      rows between 13 preceding and current row
    ) as max_price_14w
  from agg
)

select
  retail_group,
  banner,
  upc_no,
  product,
  week_end_date,
  week_index,
  revenue,
  units,
  avg_price,
  max_price_14w,
  case
    when max_price_14w is null or max_price_14w = 0 then null
    else (max_price_14w - avg_price) / max_price_14w
  end as pct_off,
  case
    when max_price_14w is null or max_price_14w = 0 then 'Regular'
    when avg_price <= max_price_14w * 0.95 then
      case
        when (max_price_14w - avg_price) / max_price_14w >= 0.20 then '20%+'
        when (max_price_14w - avg_price) / max_price_14w >= 0.10 then '10-20%'
        when (max_price_14w - avg_price) / max_price_14w >= 0.05 then '5-10%'
        else 'Regular'
      end
    else 'Regular'
  end as pct_off_bucket,
  case when avg_price <= max_price_14w * 0.95 then true else false end as is_promo_week
from ref
