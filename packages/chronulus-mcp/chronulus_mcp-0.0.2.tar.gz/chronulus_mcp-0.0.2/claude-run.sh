#!/usr/bin/env zsh


/Users/theoldfather/.local/bin/uv run \
  --prerelease=allow \
  --env-file .env \
  --with-requirements requirements.txt \
  mcp run



