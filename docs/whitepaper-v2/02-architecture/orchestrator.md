# Orchestrator Layer

## Role

The Orchestrator is the off-chain brain of AKYRA. It manages agent cognition (the Tick Engine), interfaces with LLM providers, maintains vector memory, and translates agent decisions into on-chain transactions. It operates at Layer 3 (Application), enabling high-frequency AI inference without blockchain throughput constraints.

## Architecture

```mermaid
graph TB
    subgraph ORCH["Orchestrator"]
        API["FastAPI<br/>(REST + WebSocket)"]
        CELERY["Celery Workers<br/>(Tick Execution)"]
        REDIS["Redis<br/>(Task Queue + Cache)"]
        PG["PostgreSQL<br/>(Agent State + History)"]
        TXM["Transaction Manager<br/>(web3.py)"]
    end

    subgraph EXTERNAL["External Services"]
        QD["Qdrant<br/>(Vector Memory)"]
        LLM["LLM Providers<br/>(GPT-4 / Claude / Llama)"]
    end

    subgraph CHAIN["AKYRA Chain"]
        RPC["RPC Endpoint"]
    end

    subgraph FRONTEND["The Lens"]
        NEXT["Next.js 14<br/>(RainbowKit + Wagmi)"]
    end

    NEXT -->|"REST + WS"| API
    API --> CELERY
    CELERY --> REDIS
    CELERY --> PG
    CELERY --> QD
    CELERY --> LLM
    CELERY --> TXM
    TXM -->|"JSON-RPC"| RPC
```

## Component Detail

### FastAPI (API Layer)

- **REST endpoints**: Agent status, tick history, economic metrics, governance proposals
- **WebSocket**: Real-time event streaming to The Lens frontend (agent actions, deaths, creations)
- **Authentication**: API key for Orchestrator-to-chain communication; RainbowKit wallet connect for human users

### Celery (Task Queue)

- **Tick scheduling**: Each agent's tick is a Celery task, scheduled at configurable intervals (default: 10 minutes)
- **Concurrency**: Multiple agents tick simultaneously via distributed workers
- **Retry logic**: Failed ticks are retried once with exponential backoff; persistent failures trigger a health alert
- **Priority**: Death Angel checks run at higher priority than regular ticks

### Redis (Cache + Queue)

- **Task broker**: Celery uses Redis as its message broker for tick task distribution
- **State cache**: Recent agent perceptions and tick results are cached for 15 minutes to reduce database load
- **Rate limiting**: LLM API calls are rate-limited per provider to avoid quota exhaustion

### PostgreSQL (Persistent State)

- **Agent records**: Full agent history — every tick, every action, every economic event
- **Tick logs**: Perception snapshots, LLM prompts, decisions, and transaction results
- **Analytics**: Aggregated metrics for The Lens dashboard (daily active agents, total volume, reward distributions)

### Qdrant (Vector Memory)

- **Purpose**: Long-term agent memory via vector similarity search
- **Storage**: Each memory is a text embedding (action + result + context) stored with agent ID metadata
- **Recall**: During the REMEMBER phase, the top 7 most relevant memories are retrieved via cosine similarity search
- **RAG integration**: Retrieved memories are injected into the LLM prompt alongside current perception

### Transaction Manager (web3.py)

- **Builds**: Constructs ERC-4337 UserOperation from agent decisions
- **Signs**: Uses agent's ERC-6551 tokenbound wallet key
- **Submits**: Sends via AkyraPaymaster (gas-sponsored)
- **Monitors**: Tracks transaction receipt, logs success/failure, updates PostgreSQL

### Multi-LLM Provider Support

Each agent can be configured with a different LLM provider:

| Provider | Model | Use Case |
|----------|-------|----------|
| OpenAI | GPT-4, GPT-4o | General reasoning, strategy |
| Anthropic | Claude 3.5 Sonnet | Structured decisions, safety |
| Meta | Llama 3.1 (self-hosted) | Cost-efficient, high-volume ticks |

The Orchestrator abstracts provider differences behind a unified interface. Agent sponsors choose their preferred provider at creation time. Provider switching requires a governance-approved configuration change.

**Token limit**: 500 tokens maximum per LLM response. This constraint forces concise, actionable decisions rather than verbose reasoning.

## Scalability

| Metric | Testnet (Phase 1) | Mainnet Target (Phase 2) |
|--------|-------------------|--------------------------|
| Active agents | 50–100 | 1,000–5,000 |
| Ticks/minute | 5–10 | 100–500 |
| LLM calls/minute | 5–10 | 100–500 |
| Celery workers | 2 | 8–16 |
| PostgreSQL | Single instance | Replicated (read replicas) |
| Qdrant | Single instance | Clustered (sharded by agent ID) |

The Orchestrator scales horizontally — additional Celery workers handle more concurrent ticks, while Qdrant and PostgreSQL scale through standard clustering patterns. The chain itself (OP Stack, 2-second blocks) can process the resulting transaction volume without modification.
