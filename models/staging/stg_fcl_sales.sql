with

source as (

    select * from {{ source('pos', 'raw_fcl_sales') }}

),

renamend as (
    select
        `Store Number` as store_id,
        `Product Name` as product,
        UPC as upc_no,
        CAST(`UPC` as int) as upc_int,
        CAST(`Dollar Sales` AS float64) as dollar_sales,
        CAST(`Unit Sales` AS int64) as unit_sales,
        CAST(`Week End Date` AS DATE) as week_end_date,
        retail_group,
        `Promotion Type Name` as promo_type,
        CONCAT(retail_group, '|', `Store Number`) as unique_store_id,
        CONCAT(retail_group, '|', `Store Number`, '|', `UPC`) as pod
    from
        source

)

select * from renamend
