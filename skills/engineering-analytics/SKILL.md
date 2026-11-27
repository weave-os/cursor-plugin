---
name: engineering-analytics
description: >-
  Use before any request involving Weave workspace data or tools, including
  team and individual metrics, pull requests, reviews, tasks, AI adoption,
  ambiguous entity names, and requests to post results elsewhere. Follow the
  workspace, identity, filter, and read-only rules before calling Weave MCP.
---

# Engineering analytics

Use the connected Weave MCP server for read-only analysis. For general engineering advice, leave workspace data untouched.

## When to reply without tools

- **Request to post or send.** If asked to post, send, message Slack, or share results in another app, do not query analytics or invoke any tools. Explain that Weave Analytics cannot post and offer to draft in chat. Use only figures already present in the conversation. If none are present, ask which figures and period the user wants, or offer a blank template. Never invent plausible metric values, trends, comparisons, or sources.
- **Request for a named workspace.** Treat “use the Example workspace,” “switch to Example,” “in Example Analytics,” and similar phrasing as a workspace request before extracting team names. A workspace or organization name is not a team name. Do not pass it to `resolve_entities`, list teams, or query metrics. Query only after the connection itself identifies that workspace as the one authorized by OAuth. A name in the request, a matching entity, or access to Weave tools does not identify the connected workspace. If its identity is unknown or different, explain that OAuth covers one workspace and ask the user to confirm or reconnect the intended one. End the turn without calling any tools.

## Confirm scope before requesting metrics

1. **Connection.** If a connection or required tool is unavailable, say which data you could not verify. Entity IDs cannot change the OAuth scope. Attribute results to a workspace by name only when the connection identifies it.
2. **Entities.** For every named team, person, repository or tag, call `resolve_entities` first. Search for the entity name itself, for example `Platform` for “the Platform team.” Never search for a workspace or company name as a team. If multiple plausible matches come back, give the matching names and ask which one the user means. Wait for the answer before querying metrics. If nothing matches, ask for the exact name. Use individual metrics only when requested and permitted, and preserve redactions.
3. **Filters.** Include every resolved ID in the corresponding filter on each metric or drill-down call, including when using `group_by`. For example, Platform's weekly adoption requires the resolved `team_ids` even though the result is grouped by week. If a call fails with the requested filters, report the limitation or use an equivalent query with the same scope.
4. **Dates.** Use inclusive `start_time` and `end_time` for calendar periods. Set an IANA `timezone` only when specified and keep windows and granularity consistent for comparisons. With no requested period, use and label the trailing `last_month` preset, which runs from the same date a month ago through today.

## Choose a workflow

- **Request for a specific metric.** After the workspace and any named people or teams are resolved, query only the metric and breakdown the user requested. If they ask for a monthly total or a comparison of monthly totals, skip weekly trends, per-person rates and other metrics unless the user asks for them.
- **Team or delivery snapshot.** Use `get_metric_overview` for aggregates and trends. For a team health question, start with a few relevant measures such as `code_output` (estimated engineering effort behind merged PRs), `prs` (merged PRs) and `pr_cycle_time` (median first commit to merge). For review turnaround, use `code_review_turnaround` and account for the organization’s tracking mode when interpreting the result. For task lead time, use `task_lead_time` (median in progress to completed).
- **Cycle time comparison or investigation.** Compare teams with `get_metric_overview`, `metric_type=pr_cycle_time` and `group_by=team` under the same filters and dates. For “Which PRs took the longest?”, use `get_metric_drill_down` in that scope with `metric_type=pr_cycle_time`, `sort_by="Cycle time"` and `sort_direction=desc`. Use the returned PR links and distinguish rows shown from `total_count` when results are limited.
- **AI tool adoption or code attribution.** For “What share of members used AI tools?”, use `ai_adoption_rate`, the share of eligible active members with recorded AI tool activity. Use `time_granularity=week` for a weekly trend and `group_by=ai_code_assistant` for per-tool adoption. Members can use more than one tool, so keep those shares separate. For “How many lines did assistants generate?”, use `ai_code_loc` for recorded assistant-generated LOC. For “What share of merged PR lines was attributed to AI?”, use `ai_code_percentage`, the AI share of AI-plus-human PR LOC with codegen excluded. Ask which measure the user means if “AI adoption” is used ambiguously.
- **Specific PR or metric definition.** When listed by the client, use `get_pr_details` for metadata about a known PR URL. Use `search_prs` for title or description searches only if available. For metric definitions, use `search_documentation` if available, or `get_documentation` when the tool is available and you have a Weave docs path or URL.

## Report what the data supports

- Answer in chat by default. Create a canvas, chart file or export only when the user requests that deliverable. Use an inline table when it helps compare results.
- If a metric, grouping, sort or filter is unsupported, use the available schema and error details to find an equivalent query that preserves the requested scope. Explain any gap if the requested breakdown remains unavailable.
- Report empty or partial results as such. Treat zero as a result only when the tool returns a zero count or value. Include known integration, coverage or permission limits and state which results they affect.
- Lead with the measured result, then give the metric, scope, dates and relevant units. Cite returned record or documentation links when available. For aggregate results without a link, identify the Weave metric and applied filters. Treat trends and outliers as observations and require evidence for explanations of cause.
- Describe `code_output` as estimated engineering effort or code-output units. It is not a count of lines of code. Use `ai_code_loc` for recorded assistant-generated lines, and do not infer units the tool or documentation does not establish.
- Include the first-commit-to-merge definition when reporting `pr_cycle_time`. For a specific returned pull request, include its supplied URL and label the number shown separately from the total number of matches when the query is limited.
