{% macro maxcompute__dateadd(datepart, interval, from_date_or_timestamp) %}
    {% set datepart = datepart.lower() %}
    {%- if datepart in ['day', 'month', 'year', 'millisecond', 'microsecond'] %}
       dateadd({{ from_date_or_timestamp }}, {{ interval }}, '{{ datepart }}')
    {%- elif datepart == 'hour' -%}
       dateadd(cast({{ from_date_or_timestamp }} as {{ dbt.type_timestamp() }}), {{ interval }}, '{{ datepart }}')
    {%- elif datepart == 'week' -%}
       dateadd({{ from_date_or_timestamp }}, {{ interval }}*7, 'day')
    {%- elif datepart == 'quarter' -%}
       dateadd({{ from_date_or_timestamp }}, {{ interval }}*3, 'month')
    {%- elif datepart in ['minute', 'second'] -%}
        {%- set multiplier -%}
            {%- if datepart == 'minute' -%} 60
            {%- else -%} 1
            {%- endif -%}
        {%- endset -%}
       from_unixtime(unix_timestamp(cast({{ from_date_or_timestamp }} as {{ dbt.type_timestamp() }})) + {{interval}}*{{multiplier}})
    {%- else -%}
       {{ exceptions.raise_compiler_error("macro dateadd not support for datepart ~ '" ~ datepart ~ "'") }}
    {%- endif -%}
{% endmacro %}
