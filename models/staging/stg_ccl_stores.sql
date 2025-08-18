with

source as (

    select * from {{ source('pos', 'raw_ccl_stores') }}

),

renamend as (
    select
        Geography as store_name,
        `Store Number` as store_id,
        `Division Name` as banner,
        'AB' as province,
        retail_group,
        CONCAT(retail_group, '|', `Store Number`) as unique_store_id
    from
        source

)

select * from renamend
