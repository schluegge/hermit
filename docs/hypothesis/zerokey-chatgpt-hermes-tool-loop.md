# ZeroKey ↔ ChatGPT ↔ Hermes Tool-Loop Hypothesis

**Status:** Evidence-backed hypothesis / design research  
**Date:** 2026-08-20  
**Scope:** Determine the minimum orchestration ZeroKey needs so ChatGPT.com can act as the cognition layer while Hermes remains the executable tool/runtime layer.

## Research question

Can ZeroKey mediate a multi-step tool loop where:

1. a user sends one request,
2. ChatGPT.com decides whether a tool is required,
3. ZeroKey detects the tool request,
4. Hermes executes the real tool,
5. ZeroKey feeds the real tool result back into the same model context/conversation,
6. ChatGPT may request more tools,
7. and the user receives only the final answer?

Target interaction:

```text
User
  ↓
ZeroKey
  ↓
ChatGPT.com
  ↓
Tool request?
  ├─ no  → final answer → User
  └─ yes
       ↓
    ZeroKey parser / orchestrator
       ↓
    Hermes executor
       ↓
    real tool result
       ↓
    ZeroKey reinjection
       ↓
    ChatGPT.com
       ↓
    repeat until final
```

## Current conclusion

The strongest current evidence supports the following architecture:

> ZeroKey does **not** need to become a second autonomous agent. It needs to become a small **tool-protocol adapter + turn orchestrator** between ChatGPT.com and Hermes.

Hermes can remain the owner of executable tools. ChatGPT.com can remain the cognition/model layer. ZeroKey's missing responsibility is the loop that serializes tool capabilities into model-visible instructions, recognizes structured tool intent, dispatches the call to Hermes, preserves turn/conversation state, and reinjects the real result for the next model step.

This conclusion is supported independently by two public implementations with different transport strategies:

- `aurorax-neo/chat2api`
- `Octo-Lex/ChatGPT-Web2API`

They do not prove that ZeroKey already implements this architecture. They demonstrate that the individual mechanisms are feasible and provide concrete implementation patterns.

---

## Evidence A — `chat2api`: tool protocol and model-step orchestration

Repository examined at commit:

```text
dbf6bf39686348449c25de3b6131ca733f448deb
```

Relevant files:

```text
app/service/completions.go
app/types/completions/function_calling.go
app/types/completions/function_calling_test.go
```

### Verified behavior

`chat2api` performs explicit preprocessing before sending a completion request:

```go
if err := prepareFunctionCallingRequest(apiReq); err != nil { ... }
```

Inside that preparation path it:

1. normalizes legacy function definitions,
2. detects whether tools are present,
3. detects whether prior messages contain tool results,
4. preprocesses messages when tool-call/tool-result transformation is required,
5. builds a function/tool prompt from the declared tool schemas,
6. prepends that generated protocol as a `system` message.

The relevant flow is structurally:

```text
API tool schemas
   ↓
BuildFunctionPrompt(...)
   ↓
generated system message
   ↓
existing conversation/messages
   ↓
ChatGPT request
```

This is significant because it demonstrates a model-facing tool protocol can be added as part of the request/context without making the transport itself execute the tools.

### Tool result handling

The same preparation path explicitly checks whether the message list contains prior tool results:

```go
apiReq.HasToolResults = completions.MessagesContainToolResults(apiReq.Messages)
```

and preprocesses message history before the next request:

```go
processed, err := completions.PreprocessMessages(apiReq.Messages)
```

This demonstrates the key reinjection pattern ZeroKey needs:

```text
model tool request
    ↓
external execution
    ↓
tool result represented in message/context history
    ↓
next model request
```

### Turn termination when tools appear

`chat2api` distinguishes tool-call output from ordinary assistant completion output. In its conversation loop, once aggregated tool calls are present, automatic continuation is stopped:

```go
if len(aggregated.ToolCalls) > 0 || aggregated.FinishReason != "length" {
    ...
    break
}
```

This is important for ZeroKey. A model step that requests a tool is not the final user-visible assistant answer. It is an intermediate orchestration state.

The outer system must therefore distinguish at least:

```text
MODEL_FINAL
MODEL_TOOL_REQUEST
MODEL_ERROR / INCOMPLETE
```

and only surface `MODEL_FINAL` as the end of the user's logical turn.

### Conversation state

`chat2api` tracks:

```text
ConversationId
MessageId
FinishReason
ToolCalls
ToolContent
```

and uses conversation/message identifiers for continuation behavior.

The exact representation used by ZeroKey may differ, but the architectural requirement is general: the mediator needs enough state to associate tool results with the correct model turn and conversation.

---

## Evidence B — `ChatGPT-Web2API`: authenticated ChatGPT.com transport via a real browser

Repository examined at commit:

```text
497527dceabfa3f95961e23c291e618c5570f1ac
```

Relevant files/docs:

```text
docs/architecture.md
src/chatgpt_web2api/cdp_driver.py
src/chatgpt_web2api/backend_client.py
src/chatgpt_web2api/cdp_transport.py
src/chatgpt_web2api/chatgpt_dom.py
src/chatgpt_web2api/completion_detector.py
src/chatgpt_web2api/service.py
src/chatgpt_web2api/api_server.py
src/chatgpt_web2api/mcp_server.py
```

### Verified architecture

Its documented architecture is:

```text
HTTP / MCP request
      ↓
service / handler
      ↓
CDPDriver
      ↓
real Chrome instance
      ↓
chatgpt.com web UI
```

The project deliberately drives an authenticated real browser via Chrome DevTools Protocol rather than relying purely on a separately reconstructed backend API client.

The documented message path is:

```text
1. request arrives
2. service routes to handler
3. handler calls CDP driver
4. driver navigates/selects conversation
5. text is inserted into the ChatGPT composer
6. send is triggered
7. response is observed
8. formatted result is returned
```

### Hybrid DOM/backend result acquisition

The architecture documentation explicitly describes a hybrid approach:

1. poll the DOM for response text,
2. if the DOM does not provide the authoritative content, fetch conversation data,
3. use the conversation mapping/current node for authoritative text.

This is relevant to ZeroKey because transport and output extraction do not have to be the same mechanism.

A robust ZeroKey implementation can therefore conceptually separate:

```text
transport / send
conversation identity
stream/result observation
final authoritative content extraction
```

rather than assuming one monolithic API call must provide everything.

### Multi-turn continuation

`ChatGPT-Web2API` also documents same-conversation continuation: if the current conversation is still valid, it avoids creating a fresh conversation and continues the active one.

For ZeroKey, this supports the requirement that a tool loop remain bound to one logical conversation/turn rather than spawning unrelated prompts.

---

## Combined architecture hypothesis

The two repositories cover complementary halves of the desired system:

```text
chat2api
  → demonstrates tool-protocol serialization,
    tool-call detection,
    tool-result preprocessing/reinjection,
    and conversation-step state

ChatGPT-Web2API
  → demonstrates real authenticated ChatGPT.com browser transport,
    conversation reuse,
    response observation,
    and DOM/backend hybrid extraction
```

Combined, they support this ZeroKey decomposition:

```text
┌───────────────────────────────┐
│ User / Hermes-facing caller   │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ ZeroKey Turn Orchestrator     │
│                               │
│ - conversation binding        │
│ - model-step loop             │
│ - terminal-state detection    │
│ - error/timeout handling      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ Tool Protocol Adapter         │
│                               │
│ Hermes tool registry          │
│        ↓                      │
│ model-visible contract        │
│        ↓                      │
│ parse model tool request      │
│        ↓                      │
│ normalize arguments           │
└──────────────┬────────────────┘
               │
          ┌────┴────┐
          │         │
          ▼         ▼
┌───────────────┐  ┌──────────────────┐
│ ChatGPT.com   │  │ Hermes Executor  │
│ cognition     │  │ real tools       │
└──────┬────────┘  └────────┬─────────┘
       │                    │
       │ tool request       │ real result
       └──────────┬─────────┘
                  ▼
        ┌──────────────────┐
        │ Result Reinjection│
        └────────┬─────────┘
                 │
                 └────→ next ChatGPT model step
```

---

## Minimum ZeroKey responsibilities

### 1. Tool registry projection

ZeroKey needs a deterministic way to convert Hermes's real tool inventory into a model-visible contract.

Minimum fields likely required:

```text
name
description
argument schema
result contract / representation
```

This projection must not imply that ChatGPT itself executes the tool.

### 2. Tool-call grammar

The model needs an unambiguous representation for a tool request.

Example conceptual form only:

```json
{
  "type": "tool_call",
  "id": "call_123",
  "name": "github.search",
  "arguments": {
    "query": "..."
  }
}
```

The exact syntax is still an implementation decision.

### 3. Tool-call parser

ZeroKey must distinguish tool intent from normal prose without heuristic guessing.

Required properties:

```text
strict parser
schema validation
tool-name validation
argument validation
call-id correlation
```

Malformed calls should fail deterministically rather than being executed approximately.

### 4. Hermes dispatch

Once validated, the call is handed to the Hermes-owned executable tool layer.

ZeroKey should remain mediation/orchestration, not duplicate Hermes's execution environment.

### 5. Result normalization

Hermes tool output must be converted to a representation ChatGPT can consume in the next step.

At minimum the next model step needs to know:

```text
which call the result belongs to
whether execution succeeded
actual tool output or structured error
```

### 6. Result reinjection

The result must be inserted back into the active model context/conversation before requesting the next assistant/model step.

Conceptual loop:

```text
while true:
    model_output = chatgpt(current_context)

    if model_output is final:
        return model_output

    if model_output is tool_call:
        result = hermes.execute(validated_call)
        current_context += tool_call
        current_context += tool_result
        continue

    fail deterministically
```

### 7. Turn ownership and termination

ZeroKey must know when one user-visible turn has ended.

A single user message may internally contain:

```text
model step 1
→ tool call 1
→ result 1
→ model step 2
→ tool call 2
→ result 2
→ model step 3
→ final answer
```

For the user, this should still appear as one logical request/response interaction unless intermediate visibility is explicitly desired.

---

## What the system prompt can and cannot solve

### The system prompt can provide

```text
available tool descriptions
argument schemas
required tool-call grammar
behavioral rules
instruction to wait for real tool results
instruction not to fabricate tool results
```

### The system prompt cannot by itself provide

```text
actual Hermes execution
network/process/tool dispatch
reliable validation
conversation correlation
result reinjection
repeated model invocation
loop termination
recovery after failed tool calls
```

Therefore the missing capability is not merely "more system prompt".

A prompt can define the protocol, but executable orchestration must exist outside the model.

---

## State model hypothesis

A minimal internal state object could conceptually contain:

```text
logical_turn_id
chatgpt_conversation_id
last_chatgpt_message_id
pending_tool_calls[]
completed_tool_calls[]
model_step_index
terminal_state
```

Possible terminal states:

```text
FINAL
TOOL_REQUIRED
MODEL_ERROR
TOOL_ERROR
PROTOCOL_ERROR
MAX_STEPS_EXCEEDED
CANCELLED
```

Exact field names are not prescribed; the important property is explicit state rather than implicit assumptions.

---

## Safety and correctness invariants

The following invariants should be treated as design requirements:

1. **Hermes remains execution authority.** ChatGPT may request a tool but does not fabricate execution success.
2. **No guessed tool names or arguments.** Unknown or invalid calls fail validation.
3. **Real results only.** The next model step receives the actual Hermes result or an explicit execution error.
4. **Call/result correlation is preserved.** A result cannot be associated with the wrong pending call.
5. **Conversation binding is explicit.** Tool-loop model steps stay attached to the intended ChatGPT conversation.
6. **Final answer is distinct from intermediate tool intent.** Intermediate calls are not accidentally returned to the user as completed work.
7. **Loop bounds exist.** Infinite model↔tool recursion must be prevented.
8. **Execution errors remain evidence.** They are not rewritten into success states.

---

## Open hypotheses requiring direct ZeroKey/Hermes validation

The repository evidence above does **not** yet establish the following facts about the current local ZeroKey implementation.

### H1 — Existing ZeroKey turn loop

Does ZeroKey already perform more than one ChatGPT invocation for one logical user request?

Need direct source/runtime inspection.

### H2 — Existing conversation-state representation

Does ZeroKey already preserve ChatGPT conversation ID/message ID or equivalent state across calls?

Need direct source/runtime inspection.

### H3 — Existing tool schema injection

Does the current contract-generation layer already serialize Hermes tool definitions into the ChatGPT context?

Need direct source inspection.

### H4 — Existing model-output parser

Can ZeroKey currently distinguish a tool request from final assistant prose in a deterministic machine-readable way?

Need source inspection and tests.

### H5 — Existing result reinjection path

Can ZeroKey append a real Hermes tool result and trigger the next ChatGPT model step in the same logical turn?

This is the most important unresolved capability.

### H6 — Desktop-app transport compatibility

Can the same tool loop be driven through the authenticated ChatGPT Windows desktop webview/CDP runtime instead of a standalone Chrome session while preserving the same conversation-state semantics?

Need direct runtime proof.

---

## Recommended implementation sequence

```text
M0 — Inventory current ZeroKey turn/state code
M1 — Formalize Hermes → model tool contract
M2 — Implement strict tool-call parser
M3 — Add Hermes dispatch adapter
M4 — Add result normalization + reinjection
M5 — Add bounded multi-step turn loop
M6 — Bind loop to persistent ChatGPT conversation identity
M7 — Add streaming/final-answer separation
M8 — Prove with deterministic end-to-end tests
M9 — Repeat proof using ChatGPT Windows desktop transport
```

### Minimum end-to-end proof

A useful deterministic test should require at least two real tool calls before the final answer.

Example:

```text
USER:
"Read file A, then use its value to query tool B, then tell me the result."
```

Required evidence:

```text
1. user request captured
2. ChatGPT emits tool call A
3. ZeroKey parser validates A
4. Hermes executes A
5. exact result A captured
6. result A reinjected
7. ChatGPT emits tool call B using A's real output
8. Hermes executes B
9. exact result B captured
10. result B reinjected
11. ChatGPT emits final prose
12. user receives only the final result
13. all steps share the expected logical turn/conversation identity
```

This proves actual orchestration rather than merely prompt compliance.

---

## Evidence classification

### Verified from inspected public repositories

- `chat2api` explicitly preprocesses tool-related messages.
- `chat2api` builds a tool/function prompt from supplied tool definitions.
- `chat2api` prepends that protocol as a system message.
- `chat2api` detects messages containing prior tool results.
- `chat2api` distinguishes tool-call output from ordinary terminal completion behavior.
- `chat2api` preserves conversation/message identifiers across continuation logic.
- `ChatGPT-Web2API` is architected as a CDP-driven proxy around a real ChatGPT web session.
- `ChatGPT-Web2API` separates orchestration, CDP transport, DOM interaction, backend conversation access, and completion detection.
- `ChatGPT-Web2API` documents same-conversation multi-turn continuation.
- `ChatGPT-Web2API` documents hybrid DOM + conversation-backend response acquisition.

### Evidence-supported conclusion

A ZeroKey implementation that combines:

```text
ChatGPT transport
+ tool-contract projection
+ strict tool-call parsing
+ Hermes dispatch
+ tool-result reinjection
+ bounded turn loop
```

is consistent with proven patterns in the inspected projects and matches the desired ChatGPT-as-cognition / Hermes-as-executor architecture.

### Not yet proven

- that current ZeroKey already contains all required primitives,
- that ChatGPT Windows desktop transport exposes every state primitive needed for the loop,
- that a system-prompt-only modification is sufficient,
- that the current Hermes contract format is already directly reusable without an adapter,
- or that the final architecture requires no additional persistence/recovery layer.

Those require direct inspection and reproducible testing of the local ZeroKey + Hermes implementation.
