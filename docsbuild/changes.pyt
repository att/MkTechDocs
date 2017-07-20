# Document change log

{% if numCommits == 0 %}
Looks like no changes have been committed.
{% endif %}

{% for m in gitMessages %}

{% if not m.mergeCommit %}
<p>
**Date**: {{ m.date }}<br />
**Author**: {{ m.author }}<br />
**Message**: {{ m.message }}<br />
{% endif %}

{% endfor %}
