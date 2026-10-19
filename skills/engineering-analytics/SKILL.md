---
name: engineering-analytics
description: >-
  Analyze engineering team metrics using Weave. Use when asked about
  team productivity, code output, PR cycle time, review turnaround,
  task delivery, AI coding tool adoption, agent activity, DORA metrics,
  or any engineering performance question.
---

# Engineering Analytics

Analyze engineering team performance using Weave's MCP tools. This skill handles questions about code output, PR cycle time, review quality, task delivery, AI coding tool adoption, agent activity, and more.

## When to use

- "How is my team performing?"
- "What's our PR cycle time?"
- "Who are the top contributors in the last 3 months?"
- "How much AI-written code are we shipping?"
- "Is Claude Code or Cursor driving more output for us?"
- "Show me review turnaround trends"
- "Compare team velocity month over month"
- Any question about engineering metrics, productivity, or code analytics

## Workflow

### Step 1: Understand the question

Identify what the user is asking about:
- **What metric?** Map to a specific `metric_type` (see list below)
- **What scope?** Org-wide, team, repository, or individual
- **What time range?** Default to `date_range_preset=last_month` if not specified

### Step 2: Resolve entities

If the question mentions specific teams, people, repositories, or tags, call `resolve_entities` first and use the returned IDs in later calls:
- Find a team: `resolve_entities(entity_type="team", query="Platform")`
- Find a person: `resolve_entities(entity_type="account", query="Jane")`
- Find a repository: `resolve_entities(entity_type="repository", query="backend")`
- List all teams: `resolve_entities(entity_type="team")`

Never guess IDs.

### Step 3: Fetch metrics

Choose the right tool based on the question:

- **Trends, aggregates, comparisons** → `get_metric_overview`
  - Use `date_range_preset` (`this_week`, `last_month`, `last_2_months`, `last_3_months`, `last_6_months`, `last_year`). Presets are trailing windows that end today, so for a calendar month or quarter pass `start_time` and `end_time` instead
  - Use `group_by` for breakdowns (`team`, `account`, `repository`, `pr_type`, `ai_code_assistant`, ...)
  - Use `time_granularity` for time series (`day`, `week`, `two_week`, `month`, `quarter`, `year`)
  - Use `ai_code_assistants` to filter to one tool (for example `claude_code`, `cursor_ide`, `codex`, `copilot`)

- **Specific records, outliers, investigation** → `get_metric_drill_down`
  - Use `sort_by` and `sort_direction` to find extremes
  - `total_count` is always the full match count; raise `limit` (max 300) only when you need the rows themselves

- **Broad health check** → `research_overview`
- **A specific pull request** → `search_prs`, then `get_pr_details`
- **Unusual changes** → `get_anomalies_and_trends`
- **How a metric is defined** → `search_documentation`, then `get_documentation`

Not every metric supports every `group_by` or `sort_by` value. If one isn't supported, the error lists the allowed values. Retry with one of them.

### Step 4: Present results

- Use tables for comparisons
- Round durations to human-readable values (e.g., "2.3 days" not "198432 seconds")
- Highlight trends (up/down from previous period)
- Include benchmark comparisons when available
- Call out notable outliers or patterns

## Metric reference

### Code velocity
| Metric type | What it measures |
|---|---|
| `code_output` | Expert-engineer effort behind merged PRs, estimated by Weave's models |
| `code_output_per_engineer` | Code output per engineer |
| `code_loc` | Lines of code added by PRs (move-aware) |
| `prs` | Merged PRs |
| `prs_per_engineer` | Merged PRs per engineer |
| `pr_cycle_time` | Median time from first commit to merge |
| `pr_merge_time` | Median time from PR opened to merge |
| `pr_approval_to_merge_time` | Time from approval to merge |
| `pr_deploy_lead_time` | Median time from merge to first production deploy |

### Code review
| Metric type | What it measures |
|---|---|
| `code_reviews` | PRs reviewed |
| `code_review_turnaround` | Median turnaround time for reviews given |
| `code_review_quality` | Quality of code reviews |
| `review_cycles` | Average review rounds per PR before merge |
| `pr_review_rate` | Share of PRs reviewed before merge |
| `comment_resolution_rate` | Share of review comments resolved by code changes |

### Task delivery
| Metric type | What it measures |
|---|---|
| `tasks` | Story points of completed tasks (Linear, Jira) |
| `task_count` | All tasks, any status |
| `points` | Points completed |
| `points_per_engineer` | Points completed per engineer |
| `task_lead_time` | Median time from in progress to completion |
| `task_delivery` | Median time from due date to delivery (negative means early) |
| `bug_tasks` | Tasks suspected to be bugs |

### AI coding tools and agents
| Metric type | What it measures |
|---|---|
| `ai_adoption_rate` | Share of members with any AI tool activity in the period |
| `ai_active_developers` | Engineers with AI-attributed code output |
| `ai_code_loc` | Lines added and deleted by AI tools |
| `ai_code_percentage` | % of code written by AI tools |
| `ai_output_percentage` | AI share of code output |
| `ai_code_output` | Code output from AI tools |
| `ai_efficiency_index` | Composite score combining AI output volume, usage %, cost, and code turnover |
| `output_per_ai_dollar` | AI code output per dollar of AI tool spend |
| `tool_costs` | Spend on AI tools and API usage |
| `agent_prs` | Agent-led pull requests, including open ones |
| `agent_pr_autonomy` | 1–5 score for how little human intervention agent PRs needed (higher is more autonomous) |

### Delivery and quality
| Metric type | What it measures |
|---|---|
| `ci_deploy_frequency` | Production deploys per period |
| `ci_deploy_success_rate` | % of production deploys that succeed |
| `ci_deploy_mttr` | Mean time from a failed deploy to the next successful one |
| `bugs_introduced` | Bugs introduced, from Weave's bug finder analysis |
| `bug_ratio` | Share of code output from bug-fix PRs |
| `revert_prs` | Revert PRs |
| `code_turnover` | % of code overwritten within 3 months |
| `innovation_ratio` | Share of code output from feature PRs |

## Example queries

**"How's the team doing over the last month?"**
→ `get_metric_overview` with `metric_type=code_output`, `date_range_preset=last_month`, `group_by=team`

**"Who shipped the most PRs in the last 3 months?"**
→ `get_metric_overview` with `metric_type=prs`, `date_range_preset=last_3_months`, `group_by=account`

**"What were the biggest PRs merged in the last month?"**
→ `get_metric_drill_down` with `metric_type=prs`, `date_range_preset=last_month`, `sort_by="Code output"`, `sort_direction=desc`, `limit=10`

**"What's our AI code adoption trend?"**
→ `get_metric_overview` with `metric_type=ai_code_percentage`, `date_range_preset=last_3_months`, `time_granularity=week`

**"Which AI coding tool drives the most output?"**
→ `get_metric_overview` with `metric_type=ai_code_output`, `date_range_preset=last_month`, `group_by=ai_code_assistant`

**"Compare review turnaround across teams"**
→ `resolve_entities(entity_type="team")` first, then `get_metric_overview` with `metric_type=code_review_turnaround`, `group_by=team`
