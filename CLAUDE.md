# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this workspace is

This is an AI agent workspace for **Maureen Tjahjadi**, UX Designer at Hubexo. It contains custom agents that assist with design workflow automation — not a traditional software codebase. There are no build, test, or lint commands.

**Active Claude Code project context:** PostHog project "Hubexo Mobile App Prototype" (id: 133538), organization "Hubexo".

---

## Agent: Design Impact Analyzer

Defined in `.claude/agents/design-impact-analyzer.md` (v3.6).

**Purpose:** When the upstream Impact Analysis Agent flags UI/UX work in a Jira EPIC or User Story's Task Classification, this agent reads the EPIC/User Story, queries the Breeze design ontology, and creates child Jira Tasks with structured designer + front-end handoff briefs.

**How to trigger:** Provide a Jira EPIC or User Story key (e.g. `HUB-1234`). The agent will run pre-flight checks before writing anything.

### Two-stage workflow (never skip Stage 1)

1. **Preview (Stage 1, default):** Agent shows all proposed Tasks in chat — no Jira writes. Maureen responds: `approve`, `approve except 2,3`, `revise: <feedback>`, or `cancel`.
2. **Execute (Stage 2):** Only after explicit approval. Creates Tasks in Jira and posts a summary comment on the EPIC/User Story.

Override to skip preview: say `run --execute` or "skip preview, langsung create".

### Breeze classification system

Every design surface is classified before a Task is created:

| Classification | Meaning |
|---|---|
| **REUSE** | Existing governed Breeze node, no changes needed |
| **EXTENSION** | Existing node, requires a documented new variant |
| **NET-NEW** | No node exists; proposed name flagged for Design System review |
| **DESIGN SYSTEM CONFLICT** | Requirement contradicts a governed node — Task blocked, Design Challenge raised |

**Breeze is always queried first.** If Breeze is unreachable, the agent stops.

### Stop conditions (agent exits without creating Tasks)

- Ticket type is not `Epic` or `Story`
- EPIC/User Story has no "Impact Analysis" section (upstream Impact Analysis Agent must run first)
- Task Classification does not flag UI/UX work
- Required EPIC/User Story fields missing (What / Why / Background / success metric)
- Breeze unreachable
- Architectural ↔ Design ↔ Code analyses conflict (Design Challenge raised instead)

### Task structure (four required sections, in order)

Each child Task created in Jira contains: **Background → Requirements → Suggestions → Definition of Done** (with sub-sections: Platform Required → Impacted Pages → Action Items). No additional sections. No checkboxes — plain bullets and prose only.

Task labels: `design-task-auto`, `awaiting-designer-review`. Status: default (`To Do`). Assignee: unassigned.

---

## Agent: Design Agent

Defined in `.claude/agents/design-agent.md` (v1.2).

**Purpose:** Takes a Jira Task key (from design-impact-analyzer, labelled `design-task-auto`) or a free-form prompt and produces a full design package: markdown spec, HTML prototype, and a Figma capture.

**How to trigger:** Provide a `design-task-auto` Jira Task key (e.g. `TNLM-7176`) or a free-form design brief.

### Figma output

All Figma output goes to **Claude Playground** (`fileKey: OOS3usGlcmkjMR7cPXeZA9`). One page per Jira ticket key — same ticket updates the existing page, different ticket creates a new page. After capture, the Figma link is appended to the Jira Task description under `## Figma Prototype`.

### HTML prototype

Written to `/Users/bciasia/Documents/Agent Maureen/prototypes/<kebab-surface-name>-<YYYY-MM-DD>.html`. Served locally on port 8765 for Figma capture.

---

## MCP integrations

| MCP | Agent | Used for |
|---|---|---|
| `mcp__atlassian__*` | both | Read EPICs/User Stories/Tasks; create/edit child Tasks; post comments; create issue links |
| `mcp__figma__*` (read) | both | Verify Figma components referenced by Breeze nodes; query DS libraries |
| `mcp__figma__*` (write) | design-agent only | Capture HTML prototype into Claude Playground; rename pages |
| Breeze AI | both | Read-only design ontology: governed journeys, flows, pages, components, tokens |
| PostHog | design-impact-analyzer | Product analytics — used for Insights in Task descriptions |

**Atlassian site:** `bcisuite.atlassian.net` (cloud ID: `6df8fd2f-57b9-45bd-98ad-ff70d58f7f0d`).

---

## Key rules for all agents in this workspace

- **Never write to Breeze** — read-only queries only.
- **Never modify the EPIC/User Story description** (design-impact-analyzer) — only post comments and create child Tasks.
- **Child Task descriptions** (design-agent) — the only permitted edit is appending `## Figma Prototype` after a successful Figma capture. No other sections may be touched.
- **Suggestions are proposals, not decisions** — Maureen decides. Always present options with reasoning.
- **Design Challenges** are posted as EPIC/User Story comments and route to: Solution Architect (cross-impact conflicts), Design System owner (governed-node conflicts), or Maureen (everything else).
- A Design Challenge blocks the related Task — do not create it until the challenge is explicitly resolved.
