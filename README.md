# Fortnite Macro-Analyzer (Gemini VOD Auditor)

## Overview
This is a Proof of Concept (PoC) demonstrating an asynchronous, multimodal AI pipeline. It uses Google's `gemini-2.5-flash` vision model to ingest unstructured video data (gaming VODs) and outputs a highly structured, machine-readable JSON coaching dashboard. 

To bypass the API's default 1 FPS video sampling limitation, the model uses strict System Prompt guardrails to ignore fast-paced mechanical micro-actions (aim, editing) and exclusively audit macro-strategy (zone rotations, material economy, storm surge).

## Core Technical Features
* **Pydantic Schema Enforcement:** Guarantees deterministic, structured JSON output (`application/json`) rather than conversational text.
* **Programmatic Video Metadata Slicing:** Utilizes `start_offset` parameters to dynamically trim dead air (lobby queues, loading screens) before model ingestion, optimizing token payloads.
* **Asynchronous State Handling:** Implements cloud-state while-loops to safely handle multi-minute video file processing.
* **"Anti-Ego" Guardrails:** System instructions explicitly prohibit polite/fluff responses, forcing cold, objective, error-first reporting.

## Setup & Execution
1. Install dependencies: `pip install google-genai pydantic`
2. Drop a raw gameplay video named `sample_match.mp4` into the root directory.
3. Replace the placeholder string in `fortnite_poc.py` with a valid Gemini Developer API key.
4. Run the script: `python fortnite_poc.py`
