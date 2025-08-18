with

source as (

    select * from {{ source('pos', 'raw_lcl_sales') }}

),

renamend as (
    select
        `Site Number` as store_id,
        UPC_Description as product,
        `UPC` as upc_no,
        CAST(`UPC` as int) as upc_int,
        CAST(REPLACE(REPLACE(`Sales`, '$', ''), ',', '') AS float64) as dollar_sales,
        CAST(`Units` AS int64) as unit_sales,
        CAST(REPLACE(REPLACE(`Promo Sales`, '$', ''), ',', '') AS float64) as promo_dollar_sales,
        CAST(`Promo Units` AS int64) as promo_unit_sales,
        CAST(`Week End Date` AS DATE) as week_end_date,
        retail_group,
        CONCAT(retail_group, '|', `Site Number`) as unique_store_id,
        CONCAT(retail_group, '|', `Site Number`, '|', `UPC`) as pod
    from
        source

)

select * from renamend
