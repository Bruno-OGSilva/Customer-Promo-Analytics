with

source as (

    select * from {{ source('pos', 'raw_pfg_sales') }}

),

renamend as (
    select
        Geography as store_id,
        Product as product,
        `UPC ID` as upc_no,
        CAST(`UPC ID` as int) as upc_int,
        CAST(`Dollar Sales` AS float64) as dollar_sales,
        CAST(`Unit Sales` AS int64) as unit_sales,
        CAST(`Time` AS DATE) as week_end_date,
        retail_group,
        CONCAT(retail_group, '|', Geography) as unique_store_id,
        CONCAT(retail_group, '|', Geography, '|', `UPC ID`) as pod
    from
        source

)

select * from renamend
