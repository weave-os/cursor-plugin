# Weave Analytics

Ask your engineering questions in Cursor or Claude Code and get answers from the Weave workspace your account can access. The plugin packages one shared `engineering-analytics` skill, an engineering analyst agent, and Weave's remote MCP connection.

The skill helps scope a question, select metrics and date ranges, and report the result with its limits. It covers code output, PR cycle time, review turnaround, task delivery, AI tool adoption, and related engineering analytics. Ask a question normally to use the skill when relevant. You can invoke it directly with `/engineering-analytics` in Cursor or `/weave:engineering-analytics` in Claude Code.

## Availability

The Cursor Marketplace and OpenAI plugin directory listings for version 1.1.0 are pending review and publication. Once the OpenAI listing is public, find **Weave Analytics** in the available plugin directory, install or enable it in your client, and complete Weave OAuth when prompted.

## Install in Cursor

### Local test

Cursor supports both its native plugin format and the portable Agent Plugins format. This repository includes both manifests. The native manifest is `.cursor-plugin/plugin.json`. The portable manifest is `plugin.json` at the repository root. Both discover the repository-root `mcp.json`, which defines the `weave` MCP server. Cursor's root MCP file is `mcp.json`. The `.mcp.json` file is for Claude Code.

To test locally, open an empty scratch workspace, then use **Customize → Plugins → Import from Disk** to select the repository directory. You can also copy the repository into `~/.cursor/plugins/local/weave`, then restart Cursor or run **Developer: Reload Window**. Open **Customize** and verify the skill and Weave MCP server are listed. When Cursor loads the native manifest, also verify the analyst agent. Enterprise users may need their administrator to enable local plugin imports.

If the MCP server is missing, check that the repository-root `mcp.json` is present and valid JSON, then reload Cursor. If `weave` appears twice, Cursor may be loading a prior standalone entry alongside the plugin. After verifying the new connection, disable or remove the older standalone entry at the scope where you added it.

On first use, follow the browser sign-in and authorize Weave with the account and workspace you intend to query. If sign-in did not finish, open **Customize → MCP**, select Weave, and reconnect through OAuth. Confirm that your account can access the intended Weave workspace.

### Upgrade from version 1.0.0

If you previously configured Weave with an API key, retain that configuration while installing version 1.1.0. Authorize the new plugin through OAuth and verify that its MCP connection can query your intended workspace. Then disable the older standalone Weave MCP entry at its original scope to avoid duplicate tools. To roll back, disable or uninstall the plugin in **Customize**, restore the prior standalone configuration, and reconnect it as needed.

### Marketplace install

After the Cursor Marketplace listing is public, search for **Weave Analytics** in Cursor's **Customize → Plugins** view and install it. Authenticate through the OAuth browser prompt on first use. The repository name `cursor-plugin` is retained for source compatibility.

## Install in Claude Code

After version 1.1.0 is merged into the public repository's default branch, add its marketplace and install the plugin:

```text
/plugin marketplace add weave-os/cursor-plugin
/plugin install weave@weave
```

The repository's Claude marketplace is named `weave`, and the plugin ID is `weave`. In Claude Code, run `/mcp` and verify that `plugin:weave:weave` is connected. Complete the browser OAuth flow for the intended Weave account and workspace. Ask an analytics question normally to use the shared skill, or run `/weave:engineering-analytics` directly. This GitHub-hosted marketplace has its own distribution path. Anthropic directory submission is covered in the [marketplace release guide](docs/marketplace-release.md).

If the MCP server is not connected, check `/mcp` for a connection error and reconnect through its OAuth flow. Confirm that the account can access the intended Weave workspace. If you already configured Weave as a standalone Claude MCP server, remove or disable that older entry at its original scope to avoid duplicate Weave connections. To roll back, uninstall the plugin with `/plugin`, restore the standalone server entry, then reconnect it through `/mcp`.

## Example questions

- “How did Platform's code output and median PR cycle time change last month?”
- “Compare median PR cycle time across Platform and Product for January.”
- “Show weekly AI adoption for Platform over the last month.”
- “Which merged PRs had the longest cycle time last month?”
- “What does Weave mean by `ai_adoption_rate`?”

The skill resolves named teams, people, repositories, and tags before using their identifiers in filters. If a name is ambiguous, it asks you to choose. If the tools do not support a requested metric or breakdown, it explains the gap. Trends show what changed in the returned data and do not establish a cause by themselves.

## OAuth and data

The plugin connects to `https://app.workweave.ai/public/mcp` over HTTPS. When an MCP tool runs, the client sends the request and its query parameters to Weave's MCP service. Your OAuth authorization determines which workspace data the service can return. Weave processes requests under its [privacy policy](https://weaveos.com/privacy). Do not paste passwords, access tokens, or other secrets into prompts.

OAuth handles authentication. A connected data source and Weave account access are required for the requested metrics. Results depend on connected integrations, available history, and your account permissions. For help, contact [support@workweave.ai](mailto:support@workweave.ai).

## Package contents

- `mcp.json` defines the remote MCP server for Cursor and portable Agent Plugin clients.
- `.mcp.json` defines the remote MCP server for Claude Code.
- `skills/engineering-analytics/SKILL.md` contains the shared analytics workflow.
- `agents/engineering-analyst.md` defines the analyst agent.
- `.cursor-plugin/plugin.json` is the Cursor-native manifest.
- `plugin.json` is the portable manifest and ChatGPT package metadata.
- `.claude-plugin/` contains Claude Code plugin metadata and its GitHub marketplace manifest.

Maintainers can use the [marketplace release guide](docs/marketplace-release.md). The package source is available under the MIT license. See [LICENSE](LICENSE).
