# 🚀 Lab 04: Reusable Workflows (`workflow_call`) & CD Environments

## 📌 Overview
This lab demonstrates how to build an enterprise-grade Continuous Delivery (CD) pipeline using **Reusable Workflows** in GitHub Actions. It enforces sequential environment progression (`staging` -> `production`) with environment-based protection gates.

---

## 📁 Laboratory Structure

```text
.
├── .github/
│   └── workflows/
│       ├── 04-reusable-cd.yml          # Reusable Workflow (Callable)
│       └── 04-workflow-cd-pipeline.yml # Orchestrator Workflow (Caller)
└── labs/
    └── 04-reusable-cd/
        └── README.md                   # Lab Documentation