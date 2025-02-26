{% macro partition_by(partition_config) -%}
    {%- if partition_config is none -%}
      {% do return('') %}
    {%- elif partition_config.auto_partition() -%}
        auto partitioned by (trunc_time(`{{ partition_config.fields[0] }}`, "{{ partition_config.granularity }}"))
    {%- else -%}
        partitioned by ({{ partition_config.render() }})
    {%- endif -%}
{%- endmacro -%}
