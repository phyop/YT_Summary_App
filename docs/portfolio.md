# Portfolio Collateral

## STAR resume bullets

- Reworked an API-key-dependent YouTube summarizer into a ChatGPT-authenticated Codex CLI product, removing API key onboarding while preserving structured Traditional Chinese output.
- Diagnosed a WindowsApps executable-permission conflict and built candidate-based CLI discovery that prefers the npm shim, skips inaccessible binaries, and offers a guided official CLI installation path.
- Hardened transcript processing against prompt injection by separating fixed instructions from stdin context, using read-only ephemeral Codex execution, ignoring user rules/config, and enforcing a JSON Schema.
- Reorganized the public repository into recommended `codex-cli` and archived `legacy-api` implementations, then validated unit, integration, UI, secret, and clean-clone workflows.

## LinkedIn introduction

I evolved a YouTube Traditional Chinese summary app from API-key onboarding to a ChatGPT-authenticated Codex CLI workflow. The Windows launcher creates an isolated Python environment, detects or installs the official Codex CLI, guides browser login, and launches a responsive local interface. The implementation treats transcripts as untrusted stdin context, runs Codex read-only and ephemerally, and validates output with JSON Schema. I also reproduced first-time setup from a clean clone and documented the remaining Python, Node.js, internet, and Codex-entitlement boundaries honestly.

## Conventional commit

`feat: add keyless Codex CLI summarizer`

## PR description

### Summary

Add a recommended ChatGPT-authenticated Codex CLI edition while preserving the original API edition.

### Changes

- Split the repository into `codex-cli` and `legacy-api`
- Add guided Windows setup, CLI installation, and ChatGPT login
- Add read-only ephemeral `codex exec` integration and JSON Schema output
- Add executable fallback, status endpoint, tests, and public documentation

### Testing

- Unit and Flask API tests
- Python compilation
- Real channel and transcript extraction
- Live structured Codex CLI summary
- Clean-clone installation simulation
- Desktop/mobile UI verification
- Secret scan and Git checks

### Screenshots

Validated the setup status banner, input state, summary hierarchy, and 390-pixel responsive layout locally.

### Future Work

- Timestamp citations and exports
- Cross-platform launchers
- Caching and optional local models

## Follow-on projects

- **AI Software Engineer:** add transcript caching, evaluation fixtures, streaming progress, and timestamp-grounded summaries.
- **AI Solution Architect:** design pluggable Codex, API, and local-model backends with observability and cost controls.
- **AI Agent Consultant:** build longitudinal creator research that tracks claim changes and expired forecasts.
