# NEXT_STEPS.md - Clawdbot Roadmap

Cosas para agregar y mejorar en nuestro setup de Clawdbot.

## 🔄 En Progreso

### ✅ Task Tracker System (COMPLETADO + FIXED 2026-01-28)
- [x] Sistema de seguimiento de completions para cron jobs
- [x] Auto follow-up de tareas pendientes  
- [x] ~~Detección automática de confirmaciones ("listo", "hecho", etc.)~~ → **ARREGLADO ✅**
- [x] Cron job diario para revisar pendientes (9 AM)
- [x] Created skill: `/home/sebas/clawd/skills/task-tracker/`
- [x] Setup complete with `./wrapper.sh setup`
- [x] Commands available: `./wrapper.sh [pending|complete|daily]`
- [x] **AUTO-DETECTION FIXED:**
  - ✅ `auto_detect.py` - Pattern recognition engine
  - ✅ `monitor.sh` - Message monitoring system  
  - ✅ Auto-detection cron job (every 3 minutes)
  - ✅ Completion patterns: "listo", "hecho", "completado", "done", etc.
  - ✅ **NO MORE DUPLICATE REMINDERS** 🎉

## 🚀 Próximo - Prioridad Alta

### ✅ Google Services Integration (skill gog) COMPLETADO 2026-01-28
- [x] ~~Instalar y configurar skill `gog` para conectar servicios Google~~ → SKILL FOUND ✅
- [x] **COMPLETED:** Install Go toolchain (v1.24.4 + v1.25.0 auto-upgrade)
- [x] **COMPLETED:** gog binary compilation (Linux arm64) ✅ 
  - ✅ Cloned repo: `git clone https://github.com/steipete/gogcli.git`
  - ✅ Built successfully: `make build` (~20 min on RPi)
  - ✅ Binary installed: `/usr/local/bin/gog v0.9.0`
  - ✅ Clawdbot skill status: **READY** ✓
- [x] **COMPLETED:** OAuth Configuration & Testing ✅
  - ✅ Google Cloud Console: project created & APIs enabled
  - ✅ OAuth credentials: downloaded & configured  
  - ✅ File keyring: configured with GOG_KEYRING_PASSWORD
  - ✅ Manual OAuth flow: tokens imported successfully
  - ✅ **GMAIL WORKING:** Recent emails accessible
  - ✅ **CALENDAR WORKING:** Events readable ("Pagar Alquiler y tarjeta")
  - ✅ **DRIVE WORKING:** Files listable (Europe trip docs)
  - ✅ Email account: sebastianfavaron@gmail.com authenticated
  
**🟢 STATUS: FULLY OPERATIONAL** - All Google services integrated with Clawdbot
- [ ] Test Gmail integration para lectura y envío
- [ ] Test Google Calendar para eventos y recordatorios  
- [ ] Test Google Drive para acceso a documentos
- [ ] Test Google Contacts sincronización
- [ ] **STATUS:** Skill exists in Clawdbot (✓), needs binary installation (⏳)

### 2. Smart Device Reverse Engineering & Control 🔧 NEW
*Inspired by @antonplex's Winix air purifier automation*
- [ ] **Device Discovery:** Identify "dumb" devices que pueden ser "smartificados"
  - Air purifiers, fans, heaters, AC units
  - Old appliances, audio equipment, lighting
  - Garden irrigation, pool equipment
  - Any device with IR, RS232, or network interface
- [ ] **Protocol Research:** Reverse engineer control protocols
  - Sniff network traffic, IR signals, serial communication
  - Analyze firmware, API endpoints, mobile app communication
  - Document command structures and response formats
- [ ] **Control Interface:** Create command-line tools para device control
  - Python scripts, Node.js modules, or shell wrappers
  - IR blasters, serial adapters, network injection
  - Test all device functions and edge cases
- [ ] **Clawdbot Integration:** Build skill para automated device management
  - Context-aware automation (time, weather, air quality, presence)
  - Voice control: "Turn on air purifier", "Set AC to 22°"
  - Intelligent scheduling based on patterns and conditions
  - Health/comfort optimization algorithms
- [ ] **Target Devices:** Pick first candidate for experimentation
  - Survey existing household devices
  - Research feasibility and available documentation
  - Start with simplest/most documented device

### 3. Personal Knowledge Export 🔧 IN PROGRESS
- [x] Script creado: `/home/sebas/clawd/skills/personal-export/export.sh`
- [x] Incluye MEMORY.md + memory/** + USER/IDENTITY/NEXT_STEPS/TOOLS/HEARTBEAT
- [ ] Comando `/export_personal` (alias de conveniencia)
- [ ] Formato ZIP descargable vía web UI o Telegram
- [ ] Auto-cleanup de backups antiguos

### ✅ 4. Repo de configuración (sebasfavaron) COMPLETADO 2026-02-02
- [x] **COMPLETED:** Repo remoto creado: https://github.com/sebasfavaron/clawdbot-config
- [x] **COMPLETED:** .gitignore configurado - excluye datos sensibles (memory/, USER.md, etc.)
- [x] **COMPLETED:** README.md comprensivo con documentación completa
- [x] **COMPLETED:** 13 archivos pusheados: configs, skills, setup guides
- [x] **COMPLETED:** Safe para backup/restore + sharing público
- [x] **COMPLETED:** Usa mismo token GitHub del proyecto Europa
- **🟢 STATUS: FULLY OPERATIONAL** - Repository live y sincronizado

## 🎯 Futuro - Funcionalidades Deseadas

### Knowledge Management
- [ ] Categories para knowledge base (people, projects, ideas, admin, inbox)
- [ ] Intelligent message routing (diary vs knowledge vs hybrid)
- [ ] Cross-referencing system (journal ↔ knowledge links)
- [ ] Enhanced semantic search across categories

### Voice & Media
- [ ] Whisper integration para voice-to-text
- [ ] Voice message storage en memory/audio/YYYY-MM/
- [ ] Audio transcription automática
- [ ] TTS responses para storytelling

### Automation & Intelligence
- [ ] Smart reminders con natural language parsing
- [ ] Daily digest automation con insights
- [ ] Pattern recognition en behavior y tasks
- [ ] Auto-categorization de entries

### UI/UX Improvements
- [ ] Better web UI para knowledge browsing
- [ ] Mobile-friendly interface
- [ ] Quick entry shortcuts
- [ ] Search interface improvements

### Integrations
- [ ] Notion integration
- [ ] Obsidian export compatibility
- [ ] More social channels (Discord, Slack, etc.)
- [ ] API integrations (weather, news, etc.)

## 🔧 Technical Debt

- [ ] Memory system optimization
- [ ] Better error handling en skills
- [ ] Documentation improvements
- [ ] Performance monitoring

## 📦 Storage Management (Para cuando se agregue más storage)

### ✅ Native Linux Protection (Temporalmente Activo - 02/02/2026)
**Implementado para evitar lock-outs hasta upgrade de storage:**

**1. Reserved Space Aumentado:**
```bash
sudo tune2fs -m 8 /dev/mmcblk0p2  # 8% = ~1.1GB reserved for root
```

**2. Automatic Cleanup (systemd-tmpfiles):**
```bash
# Config: /etc/tmpfiles.d/cleanup.conf
# Limpia automáticamente:
# - npm cache >3 días
# - pip/browser cache >7 días  
# - /tmp files >1 día
# - apt cache >7 días
# Runs daily via systemd-tmpfiles-clean.timer
```

**3. Efecto:** Sistema no se bloquea incluso si users llegan a 100%

### 🗑️ Cleanup Tasks (Para después del upgrade)
**Cuando se agregue más storage, remover protección temporaria:**

- [ ] Reset reserved space: `sudo tune2fs -m 5 /dev/mmcblk0p2` (back to default 5%)
- [ ] Remove aggressive cleanup: `sudo rm /etc/tmpfiles.d/cleanup.conf` 
- [ ] Remove custom protection scripts:
  - `rm scripts/memory_monitor.sh scripts/storage_manager.sh scripts/safe_install.sh scripts/daily_maintenance.sh`
- [ ] Remove daily maintenance cron (if installed)
- [ ] Verify normal systemd-tmpfiles behavior restored

**Notas:** Los scripts custom en `/home/sebas/clawd/scripts/` pueden ser útiles para otros proyectos pero no necesarios con storage adecuado.

## 📝 Ideas Vagas

- [ ] AI-powered relationship mapping
- [ ] Automatic habit tracking
- [ ] Context-aware suggestions
- [ ] Health and activity integration
- [ ] Financial tracking integration

---

**Instrucciones:**
- Mover items de "Próximo" a "En Progreso" cuando empecemos
- Marcar [x] cuando completemos
- Agregar fechas de completion
- Priorizar basado en utility actual

**Last Updated:** 2026-01-28