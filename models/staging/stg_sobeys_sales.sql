with

source as (

    select * from {{ source('pos', 'raw_sobeys_sales') }}

),

renamend as (
    select
        store_id,
        Product as product,
        `UPC No` as upc_no,
        CAST(`UPC No` as int) as upc_int,
        CAST(`Dollar Sales All Sales` AS float64) as dollar_sales,
        CAST(`Unit Sales All Sales` AS int64) as unit_sales,
        CAST(`Time` AS DATE) as week_end_date,
        retail_group,
        CONCAT(retail_group, '|', store_id) as unique_store_id,
        CONCAT(retail_group, '|', store_id, '|', `UPC No`) as pod
    from
        source

)

select * from renamend
