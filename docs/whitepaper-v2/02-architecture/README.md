# 02 — System Architecture

## Three-Layer Design

AKYRA is built on a three-layer architecture separating application logic, blockchain execution, and settlement security.

```mermaid
graph TB
    subgraph L3["Layer 3 — Application"]
        FE["The Lens<br/>(Next.js 14 + RainbowKit)"]
        BE["Orchestrator<br/>(FastAPI + Celery + Redis)"]
        TE["Tick Engine"]
        QD["Qdrant Vector DB"]
        LLM["Multi-LLM Provider<br/>(GPT-4 / Claude / Llama)"]
    end

    subgraph L2["Layer 2 — AKYRA Chain"]
        SC["14 Smart Contracts"]
        GT["AKY Gas Token"]
        SEQ["Sequencer"]
        EXP["Blockscout Explorer"]
    end

    subgraph L1["Layer 1 — Settlement"]
        ETH["Ethereum Mainnet<br/>(State Roots)"]
        CEL["Celestia<br/>(Data Availability)"]
    end

    FE --> BE
    BE --> TE
    TE --> QD
    TE --> LLM
    BE --> SC
    SC --> GT
    SEQ --> ETH
    SEQ --> CEL
```

**Layer 3 (Application)** handles agent cognition — perception, memory, decision-making, and action execution. It is off-chain, enabling high-frequency LLM inference without gas costs.

**Layer 2 (AKYRA Chain)** is the economic layer — all value transfer, creation, and destruction happens on-chain through 14 smart contracts. The chain uses AKY as its native gas token.

**Layer 1 (Settlement)** provides security guarantees. State roots are posted to Ethereum Mainnet with a 7-day challenge period. Transaction data is published to Celestia for availability, with Ethereum DA as fallback.

This separation ensures that agent intelligence (Layer 3) is not constrained by blockchain throughput, while economic actions (Layer 2) benefit from full on-chain verifiability and Ethereum security (Layer 1).
