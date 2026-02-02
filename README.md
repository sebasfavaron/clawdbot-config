# Clawdbot Configuration Repository

Personal Clawdbot agent workspace configuration and customizations.

## 🎯 Purpose

This repository preserves the configuration, skills, and customizations for a personal Clawdbot installation. It enables:

- **Disaster Recovery**: Restore complete setup after system failure
- **Documentation**: Track evolution of agent capabilities 
- **Replication**: Deploy similar setup on new hardware
- **Version Control**: Manage changes to skills and configurations

## 📁 Repository Structure

```
├── AGENTS.md           # Agent workspace guidelines
├── SOUL.md            # Agent personality and behavior
├── TOOLS.md           # Local tool notes and preferences  
├── HEARTBEAT.md       # Periodic check configuration
├── NEXT_STEPS.md      # Development roadmap and todos
├── skills/            # Custom skills and automations
├── canvas/            # Canvas presentations and demos
├── web/portal/        # Web interface customizations
└── setup-*.md         # Setup guides for integrations
```

## 🔒 Privacy & Security

**This repository does NOT contain:**
- Personal memory files (`memory/`, `MEMORY.md`)
- User profile information (`USER.md`, `IDENTITY.md`)
- Authentication credentials or API keys
- Personal data exports (`exports/`)

**Safe to share:** Configuration, skills, documentation, and generic setup guides.

## 🛠️ Key Features

### Custom Skills
- **Task Tracker**: Automated task completion detection and follow-ups
- **Personal Export**: Backup utility for personal data
- **Storage Management**: System resource protection scripts

### Integrations
- **Google Services**: Gmail, Calendar, Drive access via `gog` CLI
- **GitHub**: Repository management and CI/CD workflows
- **Web Interfaces**: Custom portal and assistant applications

### System Protection
- **Storage Monitoring**: Native Linux protection against disk exhaustion
- **Resource Management**: Prevent system lock-outs during installations
- **Automated Cleanup**: SystemD-based maintenance without cron scripts

## 🚀 Setup Instructions

1. **Clone Repository**:
   ```bash
   git clone https://github.com/sebasfavaron/clawdbot-config.git ~/clawd
   ```

2. **Install Clawdbot**: Follow [official installation guide](https://docs.clawd.bot)

3. **Restore Configuration**: 
   - Copy files to Clawdbot workspace
   - Install custom skills: `./skills/*/install.sh`
   - Configure integrations per `setup-*.md` guides

4. **Personalize**:
   - Create your own `USER.md`, `IDENTITY.md` 
   - Adjust `SOUL.md` for preferred personality
   - Initialize `memory/` directory for personal logs

## 📝 Documentation

- [Clawdbot Official Docs](https://docs.clawd.bot)
- [Community Discord](https://discord.com/invite/clawd)
- [Skill Repository](https://clawdhub.com)

## 🏗️ Development

See `NEXT_STEPS.md` for current roadmap and planned improvements.

**Last Updated**: February 2026