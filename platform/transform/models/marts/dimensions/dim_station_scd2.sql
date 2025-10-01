with
    station_scd2 as (select * from {{ ref("int_stations") }})

select *
from station_scd2
