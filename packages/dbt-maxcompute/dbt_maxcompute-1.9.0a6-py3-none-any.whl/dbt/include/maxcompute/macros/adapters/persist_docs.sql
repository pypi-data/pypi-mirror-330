{% macro maxcompute__alter_column_comment(relation, column_dict) %}
  {% set existing_columns = adapter.get_columns_in_relation(relation) | map(attribute="name") | list %}
  {% for column_name in column_dict if (column_name in existing_columns) %}
    {% set comment = column_dict[column_name]['description'] %}
    {% set escaped_comment = quote_and_escape(comment) %}

    {% if relation.is_table -%}
      alter table {{ relation.render() }} change column {{ column_name }} comment {{ escaped_comment }};
    {% else -%}
      alter view {{ relation.render() }} change column {{ column_name }} comment {{ escaped_comment }};
    {% endif -%}
  {% endfor %}
{% endmacro %}

{% macro maxcompute__alter_relation_comment(relation, relation_comment) -%}
  {{ adapter.add_comment(relation, relation_comment) }}
{% endmacro %}
