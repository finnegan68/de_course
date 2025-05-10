with source as (
    select * from "analytics"."analytics"."iris_dataset"
)

select
    cast(sepal_length as numeric) sepal_length,
    cast(sepal_width as numeric) sepal_width,
    cast(petal_length as numeric) petal_length,
    cast(petal_width as numeric) petal_width,
    species
from source