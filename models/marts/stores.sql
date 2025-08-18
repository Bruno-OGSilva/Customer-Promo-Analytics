with lcl_stores as (
    select * from {{ ref('int_lcl_stores') }}
),

fcl_stores as (
    select * from {{ ref('int_fcl_stores') }}
),

sobeys_stores as (
    select * from {{ ref('int_sobeys_stores') }}
),

ccl_stores as (
    select * from {{ ref('int_ccl_stores') }}
),

pfg_stores as (
    select * from {{ ref('int_pfg_stores') }}
),

metro_stores as (
    select * from {{ ref('int_metro_stores') }}
),

stores as (
    select * from lcl_stores
    union all
    select * from fcl_stores
    union all
    select * from sobeys_stores
    union all
    select * from ccl_stores
    union all
    select * from pfg_stores
    union all
    select * from metro_stores
)

select * from stores
