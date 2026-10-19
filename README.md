# Weave — engineering analytics for Cursor and Claude Code

Ask about your engineering team's real metrics without leaving your editor: code output, PR cycle time, review turnaround, task delivery, AI coding tool adoption, agent activity and more. Answers come from your own [Weave](https://weaveos.com) workspace.

This plugin queries your Weave data.

## What you get

### MCP server
The plugin connects your editor to Weave's remote MCP server at `https://app.workweave.ai/public/mcp`. You sign in with OAuth the first time you use it, so there is no API key to paste. Core tools:

| Tool | Description |
|---|---|
| `resolve_entities` | Find teams, people, repositories or tags by name, or look up names for IDs |
| `get_metric_overview` | Aggregated metrics with trends, time series, groupings and benchmarks |
| `get_metric_drill_down` | The records behind a metric: individual PRs, tasks and reviews |
| `research_overview` | A broad snapshot of how the organization is doing |
| `search_prs` / `get_pr_details` | Find a pull request and read its metadata |
| `get_anomalies_and_trends` | Unusual changes worth a look |
| `search_documentation` / `get_documentation` | Metric definitions and product help |

### Skill: engineering analytics
A workflow for answering analytics questions: resolve the teams or people involved, fetch the right metric, then present the result with trends and benchmarks.

### Agent: engineering analyst
An agent that thinks like an engineering leader. It leads with the finding, puts trends in context and suggests next steps.

### Cursor rule
Always-on guidance for Cursor with correct metric names, time ranges and tool order.

## Setup

### Cursor
1. Add the Weave server to `.cursor/mcp.json` (skip this step if you installed the Weave plugin from the [Cursor Marketplace](https://cursor.com/marketplace)):
   ```json
   {
     "mcpServers": {
       "weave": {
         "type": "http",
         "url": "https://app.workweave.ai/public/mcp"
       }
     }
   }
   ```
   This adds only the MCP server. To get the rule too, copy `rules/weave-analytics.mdc` into `.cursor/rules/`.
2. On first use, Cursor opens a browser window. Sign in to Weave and approve access.

### Claude Code
1. Add this repository as a plugin marketplace and install the plugin:
   ```
   /plugin marketplace add weave-os/cursor-plugin
   /plugin install weave@weave
   ```
2. Run `/mcp`, choose **plugin:weave:weave** and sign in to Weave in the browser window that opens.

## Example prompts

| Question | What happens |
|---|---|
| "How is the team doing?" | Code output, PRs and cycle time over the last month, with the trend |
| "Show me AI code adoption over time" | Weekly `ai_code_percentage` time series |
| "Which AI coding tool drives the most output?" | `ai_code_output` grouped by tool (Claude Code, Cursor, Codex, Copilot and others) |
| "Which teams have the slowest cycle time?" | `pr_cycle_time` grouped by team |
| "What were the biggest PRs merged in the last month?" | PR drill-down sorted by code output |

## Metrics

<details>
<summary><strong>Code velocity</strong></summary>

- `code_output` — Expert-engineer effort behind merged PRs, estimated by Weave's models
- `code_output_per_engineer` — Code output per engineer
- `code_loc` — Lines of code added by PRs (move-aware)
- `prs` — Merged PRs
- `prs_per_engineer` — Merged PRs per engineer
- `pr_cycle_time` — Median time from first commit to merge
- `pr_merge_time` — Median time from PR opened to merge
- `pr_approval_to_merge_time` — Time from approval to merge
- `pr_deploy_lead_time` — Median time from merge to first production deploy

</details>

<details>
<summary><strong>Code review</strong></summary>

- `code_reviews` — PRs reviewed
- `code_review_turnaround` — Median turnaround time for reviews given
- `code_review_quality` — Quality of code reviews
- `review_cycles` — Average review rounds per PR before merge
- `pr_review_rate` — Share of PRs reviewed before merge
- `comment_resolution_rate` — Share of review comments resolved by code changes

</details>

<details>
<summary><strong>Task delivery</strong></summary>

- `tasks` — Story points of completed tasks (Linear, Jira)
- `task_count` — All tasks, any status
- `points` — Points completed
- `points_per_engineer` — Points completed per engineer
- `task_lead_time` — Median time from in progress to completion
- `task_delivery` — Median time from due date to delivery (negative means early)
- `bug_tasks` — Tasks suspected to be bugs

</details>

<details>
<summary><strong>AI coding tools and agents</strong></summary>

- `ai_adoption_rate` — Share of members with any AI tool activity
- `ai_active_developers` — Engineers with AI-attributed code output
- `ai_code_loc` — Lines added and deleted by AI tools
- `ai_code_percentage` — % of code written by AI tools
- `ai_output_percentage` — AI share of code output
- `ai_code_output` — Code output from AI tools
- `ai_efficiency_index` — Composite score (volume, usage, cost, churn)
- `output_per_ai_dollar` — AI code output per dollar of AI tool spend
- `tool_costs` — Spend on AI tools and API usage
- `agent_prs` — Agent-led pull requests, including open ones
- `agent_pr_autonomy` — 1–5 autonomy score for agent PRs (higher needs less human help)

</details>

<details>
<summary><strong>Delivery and quality</strong></summary>

- `ci_deploy_frequency` — Production deploys per period
- `ci_deploy_success_rate` — % of production deploys that succeed
- `ci_deploy_mttr` — Mean time from a failed deploy to the next successful one
- `bugs_introduced` — Bugs introduced, from Weave's bug finder analysis
- `bug_ratio` — Share of code output from bug-fix PRs
- `revert_prs` — Revert PRs
- `code_turnover` — % of code overwritten within 3 months
- `innovation_ratio` — Share of code output from feature PRs

</details>

## What the plugin runs, sends and accesses

- The plugin contains no executable code. It ships a skill, an agent, a Cursor rule and one MCP server entry.
- The MCP server entry points your editor at `https://app.workweave.ai/public/mcp`. Requests go to Weave over HTTPS with an OAuth token issued to you when you sign in.
- The tools read data from your Weave workspace. They don't change anything there.
- You only see data your Weave role allows. Team members can only access data for teams they belong to.
- Weave's [privacy policy](https://weaveos.com/privacy) and [security overview](https://weaveos.com/security) cover how Weave stores and handles your data.

## Requirements

- A [Weave](https://weaveos.com) account with connected data sources (GitHub, GitLab, Bitbucket, Linear, Jira and others)

## Links

- [Weave website](https://weaveos.com)
- [Get started](https://app.workweave.ai)
- Support: support@workweave.ai

## License

MIT
