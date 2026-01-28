# Personal Knowledge Export

Creates a ZIP backup of all personal knowledge files.

## Included
- MEMORY.md (if present)
- memory/** (daily notes)
- USER.md
- IDENTITY.md
- NEXT_STEPS.md
- HEARTBEAT.md (optional)
- TOOLS.md

## Usage
```bash
./export.sh
# or
./export.sh /path/to/output-dir
```

## Output
Creates a timestamped ZIP in the output dir:
`clawdbot-personal-export-YYYYMMDD-HHMMSS.zip`
