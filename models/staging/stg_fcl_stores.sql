with

source as (

    select * from {{ source('pos', 'raw_fcl_sales') }}

),

renamend as (
    select
        `Store Name` as store_name,
        `Store Number` as store_id,
        'Federated Coop' as banner,
        Province as province,
        retail_group,
        CONCAT(retail_group, '|', `Store Number`) as unique_store_id
    from
        source

)

select * from renamend
