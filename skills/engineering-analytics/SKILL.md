---
name: engineering-analytics
description: >-
  Analyze engineering metrics from a connected Weave workspace. Use for questions
  about team code output, pull requests, review turnaround, task delivery, or
  AI tool adoption and code attribution that need actual workspace data.
---

# Engineering analytics

Use the connected Weave MCP server for read-only analysis. For general engineering advice, leave workspace data untouched.

## Set the scope and dates

- Check the client’s Weave connection and available tools. If Weave requires sign-in, ask the user to authorize or reconnect through the client’s OAuth flow for the intended organization. If the connector or a needed tool is unavailable, explain which data you cannot verify.
- Resolve named teams, people, repositories and tags with `resolve_entities`. Use the returned IDs in the corresponding filters, such as `team_ids`, `account_ids` or `repository_ids`. If “my team” is unclear or a name matches multiple plausible teams, ask the user to choose before querying metrics. A directory match establishes identity only.
- Stay within the requested scope and the signed-in user's Weave permissions. Prefer team aggregates for team questions and use individual metrics only when requested and permitted. Preserve anonymization and redactions. If access is denied, report the limitation and keep the requested scope in any follow-up queries.
- Use `start_time` and `end_time` with inclusive dates for calendar periods and an IANA `timezone` when the user specifies one. If no period is given, use the trailing `last_month` preset and label it as such. It runs from the same date a month ago through today. Use matching windows and granularity when comparing trends.

## Choose a workflow

- **Team or delivery snapshot.** Use `get_metric_overview` for aggregates and trends. For a team health question, start with a few relevant measures such as `code_output` (estimated engineering effort behind merged PRs), `prs` (merged PRs) and `pr_cycle_time` (median first commit to merge). For review turnaround, use `code_review_turnaround` and account for the organization’s tracking mode when interpreting the result. For task lead time, use `task_lead_time` (median in progress to completed).
- **Cycle time comparison or investigation.** Compare teams with `get_metric_overview`, `metric_type=pr_cycle_time` and `group_by=team` under the same filters and dates. For “Which PRs took the longest?”, use `get_metric_drill_down` in that scope with `metric_type=pr_cycle_time`, `sort_by="Cycle time"` and `sort_direction=desc`. Use the returned PR links and distinguish rows shown from `total_count` when results are limited.
- **AI tool adoption or code attribution.** For “What share of members used AI tools?”, use `ai_adoption_rate`, the share of eligible active members with recorded AI tool activity. Use `time_granularity=week` for a weekly trend and `group_by=ai_code_assistant` for per-tool adoption. Members can use more than one tool, so keep those shares separate. For “How many lines did assistants generate?”, use `ai_code_loc` for recorded assistant-generated LOC. For “What share of merged PR lines was attributed to AI?”, use `ai_code_percentage`, the AI share of AI-plus-human PR LOC with codegen excluded. Ask which measure the user means if “AI adoption” is used ambiguously.
- **Specific PR or metric definition.** When listed by the client, use `get_pr_details` for metadata about a known PR URL. Use `search_prs` for title or description searches only if available. For metric definitions, use `search_documentation` if available, or `get_documentation` when the tool is available and you have a Weave docs path or URL.

## Report what the data supports

- If a metric, grouping, sort or filter is unsupported, use the available schema and error details to find an equivalent query that preserves the requested scope. Explain any gap if the requested breakdown remains unavailable.
- Report empty or partial results as such. Treat zero as a result only when the tool returns a zero count or value. Include known integration, coverage or permission limits and state which results they affect.
- Lead with the measured result, then give the metric, scope, dates and relevant units. Cite returned record or documentation links when available. For aggregate results without a link, identify the Weave metric and applied filters. Treat trends and outliers as observations and require evidence for explanations of cause.
