# 📋 Work Dashboard

_Generated: {{ generated_at }}_

{% if pull_requests_authored %}
## 🔀 Pull Requests — Authored (waiting for review)

| # | Title | Repo | Created | Status |
|---|-------|------|---------|--------|
{% for pr in pull_requests_authored %}
| [#{{ pr.number }}]({{ pr.url }}) | {{ pr.title }} | {{ pr.repo }} | {{ pr.created }} | {{ pr.status }} |
{% endfor %}
{% endif %}

{% if pull_requests_reviewing %}
## 👀 Pull Requests — Reviewing (action needed)

| # | Title | Repo | Author | Requested |
|---|-------|------|--------|-----------|
{% for pr in pull_requests_reviewing %}
| [#{{ pr.number }}]({{ pr.url }}) | {{ pr.title }} | {{ pr.repo }} | {{ pr.author }} | {{ pr.requested }} |
{% endfor %}
{% endif %}

{% if issues %}
## 🐛 Issues Assigned

| # | Title | Repo | Priority | Labels |
|---|-------|------|----------|--------|
{% for issue in issues %}
| [#{{ issue.number }}]({{ issue.url }}) | {{ issue.title }} | {{ issue.repo }} | {{ issue.priority }} | {{ issue.labels }} |
{% endfor %}
{% endif %}

{% if ci_failures %}
## 🔴 CI/Pipeline Failures

| Repo | Branch | Pipeline | Failed at | Error |
|------|--------|----------|-----------|-------|
{% for ci in ci_failures %}
| {{ ci.repo }} | {{ ci.branch }} | [{{ ci.pipeline }}]({{ ci.url }}) | {{ ci.failed_at }} | {{ ci.error }} |
{% endfor %}
{% endif %}

{% if work_items %}
## 📌 Work Items (Azure DevOps)

| ID | Title | Project | Type | State | Iteration |
|----|-------|---------|------|-------|-----------|
{% for wi in work_items %}
| [{{ wi.id }}]({{ wi.url }}) | {{ wi.title }} | {{ wi.project }} | {{ wi.type }} | {{ wi.state }} | {{ wi.iteration }} |
{% endfor %}
{% endif %}

{% if errors %}
---
⚠️ **Warnings:**
{% for err in errors %}
- {{ err }}
{% endfor %}
{% endif %}
