with source as (
  select * from {{ source('pos', 'raw_fcl_sales') }}
),

norm as (
  select
    trim(`Store Name`)                                 as store_name,
    cast(`Store Number` as string)                     as store_id,
    'Federated Coop'                                   as banner,
    upper(trim(Province))                              as province,
    retail_group,
    concat(retail_group, '|', cast(`Store Number` as string)) as unique_store_id
  from source
)

select
  unique_store_id,
  any_value(store_id)      as store_id,
  any_value(store_name)    as store_name,
  any_value(banner)        as banner,
  any_value(province)      as province,
  any_value(retail_group)  as retail_group
from norm
group by unique_store_id
