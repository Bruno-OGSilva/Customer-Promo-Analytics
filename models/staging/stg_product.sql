with

source as (

    select * from {{ source('pos', 'raw_product_mf') }}

),

renamend as (
    select
        product,
        upc,
        CAST(upc as int) as upc_int,
        vendor,
        brand,
        category,
        subcategory,
        item_size,
        item_unit,
        pack_qty
    from
        source

)

select * from renamend
