{% test row_count_equals(model, expected_count) %}

    SELECT
        COUNT(*) as actual_count,
        {{ expected_count }} as expected_count
    FROM {{ model }}
    HAVING COUNT(*) != {{ expected_count }}

{% endtest %}
