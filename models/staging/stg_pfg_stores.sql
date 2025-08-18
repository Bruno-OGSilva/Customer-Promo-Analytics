with

source as (

    select * from {{ source('pos', 'raw_pfg_stores') }}

),

renamend as (
    select
        `Store Name` as store_name,
        `Store Number` as store_id,
        `Banner Name` as banner,
        `Province Name`,
        case
            when `Province Name` = 'ALBERTA' then 'AB'
            when `Province Name` = 'BRITISH COLUMBIA' then 'BC'
            when `Province Name` = 'MANITOBA' then 'MB'
            when `Province Name` = 'NEW BRUNSWICK' then 'NB'
            when `Province Name` = 'NEWFOUNDLAND AND LABRADOR' then 'NL'
            when `Province Name` = 'NORTHWEST TERRITORIES' then 'NT'
            when `Province Name` = 'NOVA SCOTIA' then 'NS'
            when `Province Name` = 'NUNAVUT' then 'NU'
            when `Province Name` = 'ONTARIO' then 'ON'
            when `Province Name` = 'PRINCE EDWARD ISLAND' then 'PE'
            when `Province Name` = 'QUEBEC' then 'QC'
            when `Province Name` = 'SASKATCHEWAN' then 'SK'
            when `Province Name` = 'YUKON' then 'YT'
        END as province,
        retail_group,
        CONCAT(retail_group, '|', `Store Number`) as unique_store_id
    from
        source

)

select * from renamend
