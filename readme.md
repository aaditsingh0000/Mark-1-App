# MARK L — Aven Personal AI Assistant

MARK L is a desktop personal AI assistant with voice interaction, screen/camera vision, web search, local LLM support, memory, reminders, computer controls, and an optional remote dashboard.

> **Public-release note:** this repository is designed so users provide their own credentials. **Never commit `config/api_keys.json`, `.env`, memory files, analytics files, or private TLS keys.**

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Gemini

The app accepts either:

- `GEMINI_API_KEY` as an environment variable, or
- the first-run setup screen, which stores the key locally in the **ignored** `config/api_keys.json` file.

For the environment-variable approach:

```powershell
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

macOS/Linux:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

A safe config template is provided at `config/api_keys.example.json`. It contains no real secret.

### 4. Start MARK L

```bash
python main.py
```

The first launch can ask for configuration such as the assistant name, user name, and Gemini key.

## Local LLM option

MARK L can also use a local Ollama model or an OpenAI-compatible local server. Defaults are in `core/llm_client.py` and can be overridden through the ignored local config file.

Example local settings:

```json
{
  "llm_provider": "ollama",
  "llm_url": "http://localhost:11434",
  "llm_model": "llama3.2"
}
```

For Ollama, make sure the model is installed before use:

```bash
ollama pull llama3.2
```

## Project structure

```text
Mark-L/
├── main.py                       # Application entry point and Gemini Live loop
├── ui.py                         # PyQt6 desktop UI / HUD
├── setup.py                      # Dependency + browser setup helper
├── requirements.txt              # Python dependencies
├── actions/                     # Assistant tools/actions
├── core/
│   ├── prompt.txt               # System prompt and behavior rules
│   ├── llm_client.py            # Local LLM client (Ollama/OpenAI-compatible)
│   ├── agent_router.py          # Task routing
│   └── permissions.py            # Risky-action confirmation layer
├── memory/
│   ├── memory_manager.py        # Persistent memory/session handling
│   ├── config_manager.py        # Settings + secret access
│   ├── long_term.json           # Local runtime memory template (ignored)
│   └── analytics.json            # Local runtime analytics template (ignored)
├── config/
│   ├── api_keys.example.json    # Safe public config template
│   └── api_keys.json            # Local secret/settings file (ignored)
├── dashboard/                   # Optional local/remote dashboard
└── skills/                      # Extension/skill notes
```

## Security

Before publishing or pushing changes:

```bash
git status --short
git diff -- config/api_keys.json
```

The repository ignores local secrets and runtime data, including:

- `config/api_keys.json`
- `.env` files
- `config/certs/*.key` and `config/certs/*.crt`
- `memory/long_term.json`
- `memory/analytics.json`
- `uploads/`
- Python bytecode and virtual environments

If an API key has ever been committed, copied into a public gist, or shared publicly, **revoke/rotate it in the provider console**. Removing it from Git later does not make the old credential safe.

## Diagnostics

Run the built-in diagnostics from the app, or perform a syntax check from the project root:

```bash
python -m compileall -q .
```

For a clean public checkout, the application should start with no personal memory, no analytics history, and no bundled API credentials.

## Notes

This project controls desktop applications, files, browser actions, messaging, and other system functions. Review permission prompts carefully before allowing risky actions.

## Android build

An Android starter app is included in `android/`. It provides a mobile Aven chat UI, secure on-device API-key storage, local memory, and the shared prompt asset. The original Python desktop application remains separate because desktop automation features are not directly portable to Android.
