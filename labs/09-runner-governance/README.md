# Lab 09: Runner Governance, ARC & Enterprise Policies

## Overview
Implementation and policy enforcement for GitHub Actions Runners. This lab covers runner labeling strategies, ephemeral lifecycle management with Actions Runner Controller (ARC) on Kubernetes, and enterprise security policies for isolated compute workloads.

---

## Architectural & Security Decisions

* **Ephemeral Runner Lifecycle:** Self-hosted runners in production must be ephemeral (destroyed after a single job execution) to eliminate state contamination, lateral movement, and persistent credential theft.
* **Runner Groups & Isolation:** Enterprise runner groups must be isolated by repository access level (e.g., dedicated private runner pools never exposed to public forks to prevent arbitrary code execution on internal networks).
* **Deterministic Label Routing:** Workflows target runners using explicit array matching (`runs-on: [self-hosted, linux, x64, arc-pool]`).
* **Governance Audit via Context:** Utilization of the `runner.*` context object to dynamically assert host compliance before executing pipeline payloads.

---

## Actions Runner Controller (ARC) Overview

ARC is the official Kubernetes operator that dynamically scales GitHub self-hosted runners based on webhook events and workflow demand (`AutoscalingRunnerSet`).

```text
┌────────────────────────────────────────────────────────────────────────┐
│               Actions Runner Controller (ARC) Topology                 │
│                                                                        │
│  1. Workflow Triggered (Demand) ──► GitHub Actions Controller          │
│                                            │                           │
│                                            ▼                           │
│  2. Webhook Event / Polling ────────► ARC Operator (K8s)               │
│                                            │                           │
│                                            ▼                           │
│  3. Ephemeral Pod Provisioning ─────► Creates Pod (Runner Container)   │
│                                            │                           │
│                                            ▼                           │
│  4. Job Execution ──────────────────► Pulls & Runs Step Workload       │
│                                            │                           │
│                                            ▼                           │
│  5. Post-Job Teardown ──────────────► Pod Destroyed (Clean State)      │
└────────────────────────────────────────────────────────────────────────┘