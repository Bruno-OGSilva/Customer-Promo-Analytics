with

metro_stores as (
    select * from {{ ref('stg_metro_stores') }}
),

discount_banners as (
    select `Discount Banners` as discount_banner
    from {{ source('pos', 'raw_discount_banners') }}
),

metro_stores_channel as (
    select
        store_name,
        store_id,
        banner,
        province,
        retail_group,
        unique_store_id,
        case
            when banner in (select discount_banner from discount_banners) then 'Discount'
            else 'Conventional'
        end as channel
    from metro_stores
)

select * from metro_stores_channel
