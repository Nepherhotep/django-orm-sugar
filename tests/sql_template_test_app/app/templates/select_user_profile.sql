{% autoescape off %}
  SELECT *
  FROM {{ model }}
  WHERE {{ model.name }} = {{ search_term }}
{% endautoescape %}