with

lcl_sales as (

    select * from {{ ref('stg_lcl_sales') }}

),

lcl_no_promo as (
        select
            store_id,
            product,
            upc_no,
            upc_int,
            dollar_sales,
            unit_sales,
            week_end_date,
            retail_group,
            unique_store_id,
            pod
    from lcl_sales
)

select * from lcl_no_promo
