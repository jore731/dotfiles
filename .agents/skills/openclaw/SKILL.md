---
name: openclaw
description: Configure and manage OpenClaw — the self-hosted AI gateway that connects Discord, Telegram, WhatsApp, Slack, Signal, iMessage, Matrix, Microsoft Teams, and other chat platforms to AI coding agents. Use when the user mentions OpenClaw, openclaw, gateway setup, chat channel configuration for AI agents, connecting messaging platforms to AI, multi-agent routing, agent pairing, or any task involving the openclaw CLI, openclaw gateway, or openclaw configuration files. Also use when working with openclaw config files (JSON5), SOUL.md, IDENTITY.md, or agent workspace setup.
---

# OpenClaw

OpenClaw is a self-hosted gateway that connects chat platforms (Discord, Telegram, WhatsApp, Slack, Signal, iMessage, Matrix, Microsoft Teams, Google Chat, and more) to AI coding agents. One gateway process, any channel, your own machine.

## Documentation Sources

Always fetch live documentation for specifics — OpenClaw evolves rapidly.

- **Index**: https://docs.openclaw.ai/llms.txt
- **Full reference**: https://docs.openclaw.ai/llms-full.txt
- **Installation**: https://docs.openclaw.ai/install/index.md
- **Configuration**: https://docs.openclaw.ai/gateway/configuration.md
- **Configuration reference**: https://docs.openclaw.ai/gateway/configuration-reference.md
- **CLI reference**: https://docs.openclaw.ai/cli/index.md
- **Channels overview**: https://docs.openclaw.ai/channels/index.md
- **Troubleshooting**: https://docs.openclaw.ai/help/troubleshooting.md
- **FAQ**: https://docs.openclaw.ai/help/faq.md

When helping with OpenClaw, fetch the relevant doc page for the specific topic before giving detailed instructions. Always include the doc URL in your response so the user can read the full reference. The docs are the source of truth.

## Core Concepts

- **Gateway**: The main process (`openclaw gateway`) that bridges chat channels to agent runtimes.
- **Channels**: Chat platform integrations (Discord, Telegram, WhatsApp, etc.) configured under `channels.*`.
- **Agents**: AI workspaces with isolated sessions, tools, and personalities. Configured under `agents.list[]`.
- **Bindings**: Routing rules that map inbound messages to specific agents.
- **Sessions**: Conversation state buckets, isolated per agent/channel/peer.
- **Pairing**: First-contact approval flow for new users messaging the bot.
- **SOUL.md / IDENTITY.md / USER.md**: Personality and context files loaded into agent prompts.
- **Skills**: Capabilities installed from ClawHub or local paths.
- **Nodes**: Companion devices (phones, Raspberry Pi) that extend the gateway with camera, audio, location.

## Installation Workflow

When the user wants to install OpenClaw:

1. Ask which platform (macOS local, Docker, Kubernetes, VPS, Raspberry Pi, etc.)
2. Fetch the relevant install doc: `https://docs.openclaw.ai/install/<platform>.md`
3. Walk through prerequisites, install command, and initial `openclaw configure`
4. Verify with `openclaw doctor` and `openclaw status`

Common install methods:
- **macOS**: Native app or `brew install openclaw` → bundles the gateway
- **Docker**: `docker run` with volume mounts for config and state
- **Node.js**: `npm install -g openclaw` (requires Node 20+)
- **Nix**: Flake-based install

## Configuration Workflow

OpenClaw uses JSON5 config files stored in `~/.openclaw/` (default state directory).

When helping with configuration:

1. Identify what the user wants to configure (channel, agent, model, tools, etc.)
2. Fetch the relevant config doc section
3. Use `openclaw config patch --file <patch.json5> --dry-run` to preview changes
4. Apply with `openclaw config patch --file <patch.json5>`
5. Validate with `openclaw doctor`

Key config areas:
- `channels.*` — platform credentials and policies
- `agents.list[]` — agent definitions (workspace, model, tools, sandbox)
- `bindings[]` — message routing rules
- `models.*` — model provider configuration
- `messages.*` — global message handling settings
- `session.*` — session management
- `tools.*` — tool access and policies
- `broadcast.*` — multi-agent message processing

## Channel Setup Workflow

When setting up a new chat channel:

1. Ask which channel (Discord, Telegram, WhatsApp, Slack, Signal, iMessage, etc.)
2. Fetch: `https://docs.openclaw.ai/channels/<channel>.md`
3. Guide through:
   - Creating bot/app credentials on the platform
   - Setting the token/secret securely (env var + SecretRef)
   - Configuring allowlists and policies (`dmPolicy`, `groupPolicy`)
   - Restarting/hot-reloading the gateway
   - Approving first pairing
4. Verify with `openclaw channels status --probe`

Security principles:
- Never put tokens in plain config — use SecretRef: `{ source: "env", provider: "default", id: "ENV_VAR_NAME" }`
- Use allowlists by default (`dmPolicy: "allowlist"`, `groupPolicy: "allowlist"`)
- Use access groups for shared sender lists across channels
- Run `openclaw security audit` to check for misconfigurations

## Agent Configuration

Agents are isolated workspaces with their own sessions, tools, and personality.

```json5
{
  agents: {
    list: [
      {
        id: "main",
        name: "Main Agent",
        workspace: "~/.openclaw/workspace",
        model: "anthropic/claude-sonnet-4-5",
        sandbox: { mode: "all" },
      },
    ],
  },
}
```

Key agent concepts:
- `workspace` — directory the agent operates in
- `model` — default LLM for this agent
- `sandbox` — execution sandboxing mode
- `tools` — allowed/denied tool lists
- `groupChat` — per-agent group behavior overrides

## Multi-Agent Routing

Use `bindings[]` to route messages to different agents:

```json5
{
  bindings: [
    { match: { channel: "discord", peer: { kind: "channel", id: "123" } }, agentId: "coder" },
    { match: { channel: "telegram" }, agentId: "assistant" },
  ],
}
```

Use `broadcast` for multi-agent processing of the same message (WhatsApp currently).

## CLI Quick Reference

```sh
openclaw gateway          # Start the gateway
openclaw status           # Check gateway health
openclaw doctor           # Diagnose configuration issues
openclaw doctor --fix     # Auto-fix known issues
openclaw config patch     # Apply config changes
openclaw channels status  # Check channel connectivity
openclaw pairing list     # List pending pairing requests
openclaw pairing approve  # Approve a pairing request
openclaw logs --follow    # Stream gateway logs
openclaw update           # Update OpenClaw
openclaw skills install   # Install a skill from ClawHub
openclaw agents           # List configured agents
openclaw sessions         # Manage sessions
openclaw backup           # Backup state
```

## Troubleshooting Workflow

When the user reports issues:

1. Run `openclaw doctor` to surface known problems
2. Check `openclaw status` for gateway health
3. Check `openclaw channels status --probe` for channel connectivity
4. Review logs: `openclaw logs --follow` or `~/.openclaw/logs/gateway.log`
5. Fetch relevant troubleshooting doc if needed
6. Common fixes:
   - Restart gateway after config changes
   - Verify tokens/secrets are set in environment
   - Check allowlists include the user's ID
   - Verify platform bot permissions (intents, scopes, etc.)

## Model Configuration

OpenClaw supports multiple model providers (Anthropic, OpenAI, local models, etc.):

```json5
{
  models: {
    providers: {
      anthropic: { apiKey: { source: "env", id: "ANTHROPIC_API_KEY" } },
      openai: { apiKey: { source: "env", id: "OPENAI_API_KEY" } },
    },
  },
}
```

Use `openclaw models` CLI to list and manage available models. Model failover is configurable for resilience.

## Key Principles

- **Fetch live docs** before giving detailed setup instructions — things change fast
- **Security first** — tokens via SecretRef, allowlists by default, sandbox agents
- **Verify changes** — always `--dry-run` before applying config, then `openclaw doctor`
- **One gateway, many channels** — design for the user's multi-platform setup
- **Session isolation** — each agent/channel/peer combination has its own context
