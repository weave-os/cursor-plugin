# Weave — Engineering Analytics for Cursor

Query your engineering metrics directly from Cursor. Get instant answers about code velocity, PR cycle time, review quality, AI code adoption, and 40+ other metrics without leaving your editor.

**[Get your API key →](https://app.workweave.ai/organization/settings)**

## What you get

### MCP server
Four tools connected to your Weave workspace:

| Tool | Description |
|---|---|
| `get_metric_overview` | Aggregated metrics with trends, time series, and benchmarks |
| `get_metric_drill_down` | Detailed records behind any metric — individual PRs, tasks, reviews |
| `get_accounts` | Team member names and IDs for filtering |
| `get_teams` | Team names and IDs for filtering |

### Rules
Pre-configured guidance that teaches the AI how to use Weave tools effectively — correct metric names, date formats, and best practices.

### Skill: Engineering Analytics
A structured workflow for answering complex analytics questions: resolving entities, fetching the right metrics, and presenting actionable insights.

### Agent: Engineering Analyst
A purpose-built agent persona that thinks like an engineering leader — it leads with insights, contextualizes trends, and suggests next steps.

## Setup

1. **Install the plugin** from the [Cursor Marketplace](https://cursor.com/marketplace)
2. **Add your API key** in Cursor Settings:
   - Open Cursor Settings (`Cmd+Shift+J`)
   - Go to **Tools & MCP**
   - Find the **weave** server and click the edit (pencil) icon
   - Replace `YOUR_WEAVE_API_KEY` with your actual key (e.g., `wkey_abc123...`)
   - Restart Cursor for the change to take effect
3. **Start asking questions** in Cursor chat:
   - "What's our PR cycle time this month?"
   - "Compare code output across teams for Q1"
   - "How much AI-written code are we shipping?"
   - "Who has the longest review turnaround?"

## Example prompts

| Question | What happens |
|---|---|
| "How is the team doing?" | Fetches code output, PRs, and cycle time for the last 30 days with trend comparison |
| "Show me AI code adoption over time" | Returns weekly `ai_code_percentage` time series |
| "Which repos have the slowest cycle time?" | Drills down into `pr_cycle_time` grouped by repository |
| "Compare our review quality to benchmarks" | Fetches `code_review_quality` with organization benchmarks |

## Available metrics

<details>
<summary><strong>Code velocity</strong></summary>

- `code_output` — Weighted productivity score
- `code_output_per_engineer` — Per-person output
- `code_loc` — Lines of code changed
- `prs` — Pull requests merged
- `prs_per_engineer` — PRs per person
- `pr_cycle_time` — Open to merge duration
- `pr_merge_time` — Approval to merge duration
- `pr_deploy_lead_time` — Merge to deploy duration

</details>

<details>
<summary><strong>Code review</strong></summary>

- `code_reviews` — Reviews performed
- `code_review_turnaround` — Time to first review
- `code_review_quality` — Review thoroughness score
- `review_cycles` — Review rounds before merge
- `pr_review_rate` — % of PRs reviewed
- `comment_resolution` — Comment resolution details
- `comment_resolution_rate` — Resolution rate

</details>

<details>
<summary><strong>Task delivery</strong></summary>

- `tasks` — Tasks completed
- `task_count` — Total task count
- `points` — Story points delivered
- `points_per_engineer` — Points per person
- `task_lead_time` — Creation to completion
- `task_delivery` — Delivery rate
- `bug_tasks` — Bug tasks

</details>

<details>
<summary><strong>AI code</strong></summary>

- `ai_code_loc` — AI-assisted lines of code
- `ai_code_percentage` — % of code written with AI
- `ai_output_percentage` — AI share of code output
- `ai_efficiency_index` — Composite score (volume, usage, cost, churn)
- `output_per_ai_dollar` — Output per AI dollar
- `tool_costs` — AI tool costs

</details>

<details>
<summary><strong>Quality</strong></summary>

- `bugs_introduced` — Bugs introduced
- `bug_ratio` — Bug-to-feature ratio
- `revert_prs` — Reverted PRs
- `code_turnover` — Code churn
- `innovation_ratio` — Feature vs maintenance ratio

</details>

## Requirements

- A [Weave](https://weaveos.com) account with connected data sources (GitHub, GitLab, Linear, Jira, etc.)
- An API key from your [Weave settings](https://app.workweave.ai/organization/settings)

## Links

- [Weave website](https://weaveos.com)
- [Get started](https://app.workweave.ai)
