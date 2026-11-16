# Dappy Dogs AI Chatbot API

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Version](https://img.shields.io/badge/Version-0.1.0-informational)
![Task](https://img.shields.io/badge/Task-AI%20Chatbot-ED4D6C)
![Last Updated](https://img.shields.io/badge/Last%20Updated-Nov%202026-brightgreen)

*Conversational access to Dappy Dogs profile, activity, and care data.*

This repository contains the backend API and AI orchestration layer for the chatbot integrated into the Dappy Dogs mobile application. The service provides controlled natural-language access to dog profiles, walks, activity statistics, and owner-provided care records while preserving authentication and data isolation boundaries.

## Contents

- [Scope](#scope)
- [Core principles](#core-principles)
- [Architecture](#architecture)
- [Development](#development)
- [Status](#status)

## Scope

The initial product scope includes:

- Questions about dog profiles, walks, and recorded activity.
- Deterministic totals, averages, and basic activity comparisons.
- Confirmed creation and retrieval of vaccine, deworming, medication, and appointment records.
- Basic chatbot usage instrumentation.

Veterinary diagnosis, treatment recommendations, proprietary model training, smart-device integration, document extraction, real-time monitoring, social features, proactive notifications, and advanced analytics are outside the initial scope.

## Core principles

- The authenticated backend identity governs every data access.
- Users can access only their own authorized dogs and account data.
- The language model never accesses Firebase directly.
- Model-requested actions are allowlisted, typed, authorized, and validated by the application.
- Care-record changes require explicit user confirmation before persistence.
- Activity statistics are calculated by deterministic application code.
- The chatbot does not provide veterinary diagnoses or treatments.
- Logs and telemetry exclude secrets, raw conversations, and sensitive record contents.

## Architecture

The service is planned as a modular Python API with explicit boundaries between HTTP transport, application use cases, domain policies, Firebase persistence, authentication, telemetry, and the language-model provider.

```mermaid
flowchart LR
    APP["Dappy Dogs mobile app"]
    API["Chatbot API"]
    AUTH["Authentication"]
    FB["Firebase / Cloud Firestore"]
    LLM["Language model provider"]
    METRICS["Usage metrics"]

    APP -->|Authenticated HTTPS| API
    API -->|Verify identity| AUTH
    API -->|Authorized reads and writes| FB
    API -->|Minimized structured context| LLM
    API -->|Privacy-minimized events| METRICS
```

Technology choices beyond Python 3.14 remain subject to technical discovery of the existing mobile application, Firebase schema, authentication flow, and deployment environment.

## Development

The repository is in its foundation stage. Once the Python package and development dependencies are defined, the standard command interface will be:

```bash
make install-dev
make format
make format-check
make lint
make test
make check
```

On Windows, the commands use `.venv/Scripts/python.exe`; on POSIX systems, they use `.venv/bin/python`.

## Status

Version `0.1.0` establishes the repository foundation. Application code, dependency metadata, executable tests, infrastructure adapters, and deployment configuration are not yet included.
