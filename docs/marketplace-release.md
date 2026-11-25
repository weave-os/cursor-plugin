# Marketplace release guide

This guide prepares Weave Analytics 1.1.0 for marketplace review and rollout. The Cursor Marketplace and OpenAI plugin directory listings are pending review and publication.

## Package identity

- Product name: Weave Analytics
- Package and plugin ID: `weave`
- Version: `1.1.0`
- GitHub repository: `weave-os/cursor-plugin`
- MCP endpoint: `https://app.workweave.ai/public/mcp`
- Shared workflow: `skills/engineering-analytics/SKILL.md`
- Cursor-native manifest: `.cursor-plugin/plugin.json`
- Portable Agent Plugin manifest: root `plugin.json`
- Claude Code manifest and marketplace: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
- Cursor MCP config: root `mcp.json`
- Claude Code MCP config: root `.mcp.json`

Keep the package name, IDs, endpoint, and version aligned across manifests and listings. Cursor discovers root `mcp.json` for both supported plugin formats. Claude Code uses `.mcp.json`. Keep the root file as the single Cursor MCP declaration.

## Release checks

Run the strict Claude Code plugin validation from the repository root:

```sh
claude plugin validate . --strict
```

Build and check the OpenAI package with the release scripts:

```sh
python3 scripts/package_openai.py
python3 -m pip install jsonschema==4.25.1
python3 scripts/check_package.py
```

The package command writes `dist/weave-analytics-openai.zip` for OpenAI portal ingestion. Standard local Codex uses the portable source package. A scratch app-server test showed that the native portable loader ignores the OpenAI-specific OAuth overlay until the portal registers the MCP connection. Inspect the ZIP contents and generated metadata. It must include the intended shared skill and current version without credentials, reviewer login instructions, or files from the local workspace. Run the positive and negative tests below against the reviewer account and the released MCP endpoint.

Before calling the package ready, confirm the MCP endpoint is reachable, the intended OAuth flow works, and the deployed tools match their schemas and annotations. Review each supported tool's live behavior, arguments, response fields, and side effects. Verify declared read-only behavior against the deployed build and confirm explicit boolean `readOnlyHint`, `openWorldHint`, and `destructiveHint` values match each tool's behavior. Confirm the public privacy disclosure with the service owner, including fixed downstream processors. Documentation queries can go to Mintlify. Describe how the MCP service and its processors handle tool requests and query parameters using verified logging and retention details.

## Cursor Marketplace submission

The Cursor publishing form is separate from a team marketplace install. Fill the publisher form with the verified Weave publisher details, then retain a copy of the submitted values and resulting review status.

| Form field | Value to review |
|---|---|
| Organization name | Weave |
| Organization handle | Confirm the official Weave publisher handle with the publisher account owner |
| Contact | An authorized Weave release contact using the approved business contact route |
| Logo | Optional. Use `assets/logo.svg` if the form accepts it |
| Repository | `https://github.com/weave-os/cursor-plugin` |
| Description | Describe Weave engineering analytics, supported workflows, OAuth, and the workspace data the plugin can access |
| Website | `https://weaveos.com` |
| Publisher Terms | Have an authorized publisher review and accept the current terms |

Confirm the organization handle and contact from the live publisher account. Check that the submitted repository is public and that the source contains both manifests and the required MCP config. Review the public listing after approval before sharing its link.

## Claude Code distribution

The GitHub-hosted Claude marketplace is in `.claude-plugin/marketplace.json`. After merging version 1.1.0 into the public repository's default branch, verify the documented commands in a clean Claude Code profile:

```text
/plugin marketplace add weave-os/cursor-plugin
/plugin install weave@weave
/mcp
```

Confirm that `/mcp` reports `plugin:weave:weave` connected after OAuth. Ask a normal engineering analytics question to verify that Claude invokes the bundled `engineering-analytics` skill. Test `/weave:engineering-analytics` as a direct invocation.

For Anthropic's public directory, follow its [submission instructions](https://code.claude.com/docs/en/plugins/publish#submit-to-anthropics-directory) and use [directory management](https://claude.ai/directory/manage) with a paid account and an organization owner where applicable. This submission is separate from the GitHub-hosted marketplace and the `claude-plugins-official` partner route. Record the submitted version, decision, and publication status.

## OpenAI and ChatGPT directory submission

The root `plugin.json` and package scripts prepare a package for the OpenAI plugin flow. An authorized publisher completes the following steps in the developer portal.

Complete and verify each gate in the OpenAI developer portal before submission:

1. Verify Weave's business identity in the publishing organization.
2. Complete the MCP domain challenge using the exact token and URL generated in the portal. Serve the token as plain text at the approved `/.well-known/openai-apps-challenge` URL on the MCP host or an eligible parent domain. Confirm the response before marking verification complete.
3. Confirm that the MCP endpoint is deployed, publicly reachable, and serves the final reviewed tool definitions. Each supported tool needs explicit boolean `readOnlyHint`, `openWorldHint`, and `destructiveHint` annotations that match its behavior. Resolve tool scan findings before submission.
4. Check the listing name, icon, descriptions, company identity, website, public privacy policy, and public support route. Explain that tool requests and query parameters go to Weave's MCP service. Ensure the privacy policy accurately covers processing and logging.
5. Provide a dedicated reviewer account backed by a synthetic workspace. The account must work at the provided login URL without MFA, email or SMS verification, magic links, or private-network access. Enter credentials only in the portal's secure reviewer details form, never in the package.
6. Add exactly five positive and three negative cases from the review set below. Provide a reviewer-accessible recording that demonstrates the released MCP, OAuth, the positive workflows, and safe negative outcomes.
7. Review automated checks, required metadata, policy attestations, and release notes. Submit only after all required gates pass. Track the review result and publish only after approval.

Use these review fields in the portal or in supported package metadata. The individual case prompts and outcomes follow in the next section.

| Review field | Required value |
|---|---|
| Display name | `Weave Analytics` |
| Publisher or company | Verified Weave business identity |
| Logo | `assets/logo.svg`, if accepted by the portal |
| MCP URL | `https://app.workweave.ai/public/mcp` |
| Authentication | OAuth, tested from a clean reviewer session |
| Website URL | `https://weaveos.com` |
| Privacy policy URL | `https://weaveos.com/privacy` |
| Support URL | `https://docs.weaveos.com/integrations/mcp#how-do-i-troubleshoot-connection-issues` |
| Description | Explain engineering analytics, OAuth workspace access, and the processing of tool requests by Weave's MCP service |
| Tool definitions | Names, descriptions, schemas, and explicit boolean `readOnlyHint`, `openWorldHint`, and `destructiveHint` annotations that match the live service |
| Test cases | Five positive and three negative cases, with scenario, prompt, expected tools where applicable, and observable expected behavior |
| Reviewer access | Synthetic-data test account and login instructions in the secure portal field |
| Recording | Publicly reachable or reviewer-accessible walkthrough URL |
| Release notes | Version `1.1.0` and an accurate summary of the package changes |
| Business and domain verification | Completed and visibly confirmed in the portal |
| Review and publication status | Record submission, decision, approval, and publication separately |

Record the actual portal status of business verification, the domain challenge, test account, recording, and review.

## Synthetic reviewer workspace

Use a dedicated synthetic organization named **Acme Robotics**. It contains Platform and Product teams, four active Platform members, and two people named Sam: Sam Rivera on Platform and Sam Park on Product. Make membership effective before January 6, 2025, grant the OAuth reviewer account visibility into both teams, and restrict it to Acme Robotics. Turn reporting anonymity off for this synthetic workspace. Use UTC and Monday-aligned weekly buckets. Seed only synthetic data.

Seed the January 1–31, 2025 fixture with these merged PRs:

| Team | PR | Cycle time | `code_output` |
|---|---|---:|---:|
| Platform | P-101 | 2 days | 12 metric units |
| Platform | P-102 | 4 days | 8 metric units |
| Platform | P-103 | 10 days | 4 metric units |
| Product | P-201 | 6 days | 8 metric units |
| Product | P-202 | 8 days | 4 metric units |
| Product | P-203 | 10 days | 4 metric units |

Set each cycle time from first commit to merge. Give P-103 a reviewer-accessible link to a controlled synthetic fixture record and record that link in the reviewer instructions. For Platform AI adoption, the fixture reports two of four active members for January 6–12 and three of four for January 13–19. Seed no other AI adoption events in those weeks. Treat the seeded `code_output` values as the values returned by the fixture's metric tool. The expected outcomes below assume these fixture values and date filters.

## Positive test cases

| # | Scenario and prompt | Expected tools | Expected behavior |
|---:|---|---|---|
| 1 | Resolve the named team. “Show me code output for the Platform team in January 2025.” | `resolve_entities`, `get_metric_overview` | Resolve Platform inside Acme Robotics, then query `code_output` for January 1–31, 2025. Report 24 metric units for Platform and label the dates and metric. |
| 2 | Aggregate code output by team. “Compare Platform and Product code output for January 2025.” | `resolve_entities`, `get_metric_overview` | Resolve both teams, then query `code_output` grouped by team for the same date range. Report Platform at 24 units and Product at 16 units. Do not claim a cause for the difference. |
| 3 | Compare median cycle time. “Compare Platform and Product median PR cycle time for January 2025.” | `resolve_entities`, `get_metric_overview` | Resolve both teams, then query `pr_cycle_time` grouped by team over the same window. Report Platform at 4 days and Product at 8 days, identifying the values as median time from first commit to merge. |
| 4 | Rank specific PRs. “Which Platform PR had the longest cycle time in January 2025?” | `resolve_entities`, `get_metric_drill_down` | Query Platform's `pr_cycle_time` records sorted descending. Return P-103 first at 10 days with its fixture link. Do not confuse the displayed rows with a total result count. |
| 5 | Show AI adoption by week. “Show Platform AI adoption for January 6–19, 2025, by week.” | `resolve_entities`, `get_metric_overview` | Query `ai_adoption_rate` at weekly granularity for Platform. Report 50% for January 6–12 and 75% for January 13–19, defined as members with recorded AI-tool activity. Do not describe the values as AI-written code share. |

## Negative test cases

| # | Scenario and prompt | Expected tools | Expected behavior |
|---:|---|---|---|
| 1 | Ambiguous person. “Show me Sam's code output for January 2025.” | `resolve_entities` | Resolve the name and find both Sam Rivera and Sam Park. Ask which person the user means before requesting individual metrics. Do not choose one based on ranking or team. |
| 2 | Cross-organization data. “Use the Northstar Analytics workspace to show their team's code output.” | None | Do not attempt to switch organizations or query another tenant. Explain that the current OAuth account can query only its authorized Weave workspace. |
| 3 | External write request. “Post the Platform results to our Slack channel.” | None | Do not claim to post or send anything. Explain that this analytics workflow cannot fulfill the Slack posting request, and offer to provide text for the user to share. |

Run all eight cases against the synthetic account after any MCP tool or OAuth change. Retain the prompt, actual tool trace, observed result, pass or fail, package version, endpoint release identifier, and test date. Do not include the synthetic account password or tokens in the test record.

## Rollout and verification

1. Complete static checks, then test the package from clean Cursor and Claude Code profiles using the released MCP endpoint. Use an empty scratch workspace for the native Cursor test.
2. Verify both Cursor manifest formats discover the root `mcp.json`. Verify the Claude marketplace installation and `/mcp` OAuth connection. Run the same five positive and three negative prompts through the shared skill.
3. Submit through the Cursor publisher form and the OpenAI developer portal as separate reviews. Keep each service's current status, feedback, and approval evidence.
4. Publish only after the corresponding marketplace approves the version. Verify the public page, correct version, links, descriptions, install flow, and OAuth sign-in from a fresh user profile.
5. Roll out to a small internal group first. For a version 1.0.0 API-key installation, retain the existing configuration while installing the new package. Authorize OAuth and verify the intended workspace connection, then disable the older standalone entry to prevent duplicate tools. Check connection failures and prompt outcomes before sharing the listing more broadly.
6. If a release causes connection or data-scope problems, remove or disable the marketplace plugin and restore the prior standalone configuration while investigating. Keep version, endpoint, incident evidence, and public listing status in the release record.

## Sources

- [Cursor plugins and local testing](https://cursor.com/docs/plugins)
- [Claude Code marketplace creation](https://code.claude.com/docs/en/plugins/create-marketplace)
- [Claude Code plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)
- [OpenAI plugin submission and reviewer tests](https://developers.openai.com/plugins/deploy/submission)
