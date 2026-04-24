"""config.py — Configurações centrais"""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = os.getenv("CLAUDE_MODEL", "claude-opus-4-5")
VERBOSE           = os.getenv("VERBOSE", "true").lower() == "true"
OUTPUT_DIR        = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY não encontrada no .env")
