with lcl_sales as (
    select * from {{ ref('int_lcl_sales') }}
),

fcl_sales as (
    select * from {{ ref('int_fcl_sales') }}
),

sobeys_sales as (
    select * from {{ ref('stg_sobeys_sales') }}
),

ccl_sales as (
    select * from {{ ref('stg_ccl_sales') }}
),

pfg_sales as (
    select * from {{ ref('stg_pfg_sales') }}
),

metro_sales as (
    select * from {{ ref('stg_metro_sales') }}
),

sales as (
    select * from lcl_sales
    union all
    select * from fcl_sales
    union all
    select * from sobeys_sales
    union all
    select * from ccl_sales
    union all
    select * from pfg_sales
    union all
    select * from metro_sales
)

select * from sales
