# Agent interoperability protocols

Verification date: 2026-08-19

## MCP — Model Context Protocol

**Definition / role.** MCP is an open protocol for integrating LLM applications with external data sources and tools. The official specification defines hosts, clients, and servers and standardized context/tool integration.

**Current version evidence.** The MCP project announced specification revision `2026-07-28` on 2026-07-28. The release changed the protocol core to stateless operation and added Multi Round-Trip Requests, header-based routing, cacheable list results, authorization hardening, an extensions framework, and SDK updates.

**Representative protocol capabilities.** Earlier official specification pages establish the stable conceptual primitives: resources, prompts, and tools, with JSON-RPC-based messaging. Because the July 2026 revision changed core lifecycle/session behavior, implementations must verify behavior against the current revision rather than assume 2025 session semantics.

**Selection criteria.** Use MCP when an AI host/agent needs standardized access to tools, data/context, or composable external capabilities. Evaluate current protocol revision support, transport/authentication support, security/consent model, SDK maturity, and server provenance.

**Integration points.** AI hosts, coding agents, data systems, developer tools, service APIs, context providers.

**Automation possibilities.** Tool invocation, context retrieval, structured resources, composable workflows, and agent-accessible external operations. Each tool's side effects and authorization remain application-specific.

Sources:
- MCP 2026-07-28 release announcement — https://blog.modelcontextprotocol.io/posts/2026-07-28/ (official project blog; published 2026-07-28; verified 2026-08-19).
- MCP specification overview (2025-11-25 historical revision) — https://modelcontextprotocol.io/specification/2025-11-25 (official specification; verified 2026-08-19). Used only for conceptual primitives; superseded for current lifecycle details.

## A2A — Agent2Agent Protocol

**Definition / role.** A2A is an open standard for communication and collaboration between independent, potentially opaque AI agent systems built with different frameworks, languages, or vendors. Its protocol goal includes capability discovery, modality negotiation, collaborative task management, and secure exchange without requiring access to another agent's internal state, memory, or tools.

**Current version evidence.** Official A2A documentation currently presents release `1.0.0` as the latest released version.

**Selection criteria.** Use A2A for agent-to-agent interoperability when the boundary is between independently operating agent systems rather than between an agent and a tool/data provider. Verify version compatibility, authentication/authorization requirements, supported transports/modalities, task semantics, and SDK/framework support.

**Integration points.** Multi-agent systems, cross-vendor delegation, remote agent discovery, collaborative task exchange. A2A and MCP are complementary rather than substitutes: A2A targets agent-agent communication, MCP targets model/agent access to context and tools.

**Automation possibilities.** Agent discovery, task delegation, collaborative execution, cross-agent result exchange, and multi-agent workflow composition.

Sources:
- A2A v1.0 documentation — https://a2a-protocol.org/v1.0.0/ (official protocol docs; verified 2026-08-19).
- A2A specification repository — https://github.com/a2aproject/A2A/blob/main/docs/specification.md (primary repository; observed as latest released version 1.0.0; verified 2026-08-19).

## ACP — Agent Client Protocol

**Definition / role.** ACP is an open protocol created by Zed for interoperability between coding agents and editing environments. It standardizes the editor/client ↔ agent boundary so an ACP-speaking agent can integrate with ACP-compatible editing environments without a bespoke integration per pairing.

**Representative verified capabilities.** Zed documents ACP integrations exposing editor-side capabilities including multi-file editing and codebase context, and lists multiple ACP-compatible editors and agents.

**Selection criteria.** Use ACP when the integration boundary is specifically an interactive coding agent and an editor/client UI. Evaluate editor and agent implementation support, protocol/version compatibility, transport, permissions, context exposure, and whether an adapter is required.

**Integration points.** IDE/editor agent panels, coding-agent CLIs, code review/edit workflows, terminal streaming and code-context exchange depending on implementation.

**Automation possibilities.** Standardized agent sessions inside editors, code-context transfer, edit/review interactions, and reuse of one agent across multiple ACP clients.

**Boundary with MCP/A2A.** ACP is not interchangeable with MCP or A2A. ACP addresses editor/client ↔ coding-agent interoperability; MCP addresses AI ↔ tools/context; A2A addresses independent agent ↔ agent communication. A system may legitimately use more than one.

Source:
- Zed ACP overview — https://zed.dev/acp (protocol creator documentation; verified 2026-08-19).