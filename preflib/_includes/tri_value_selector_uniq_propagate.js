
{% for value in include.values %}
    const {{ value }}selectorYes = document.getElementById('selector-{{ value }}-yes');
    const {{ value }}selectorNo = document.getElementById('selector-{{ value }}-no');
    const {{ value }}selectorIndef = document.getElementById('selector-{{ value }}-indef');
    {{ value }}selectorYes.addEventListener("change", function(evt) {
        {% for t in include.values %}
            {% if t != value %}
                {{ t }}selectorNo.checked = true;
            {% endif %}
        {% endfor %}
    })
    {{ value }}selectorIndef.addEventListener("change", function() {
        {% for t in include.values %}
            {% if t != value %}
                if ({{ t }}selectorYes.checked) {
                    {{ t }}selectorIndef.checked = true;
                }
            {% endif %}
        {% endfor %}
    })
{% endfor %}