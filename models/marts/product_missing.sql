with product as (
    select * from {{ ref('stg_product') }}
),

sales as(
    select * from {{ ref('sales') }}
),

product_missing as (
    select
    a.product,
    a.upc_no,
    a.retail_group,
    b.brand
from sales a
left join product b
    on a.`upc_no` = b.`upc`
where b.brand IS NULL
)

select * from product_missing
