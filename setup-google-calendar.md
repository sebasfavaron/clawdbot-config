# Setup Google Calendar API

## 1. Google Cloud Console
1. Ve a https://console.cloud.google.com/
2. Crear nuevo proyecto o usar uno existente
3. Habilitar Google Calendar API:
   - APIs & Services > Library
   - Buscar "Google Calendar API"
   - Hacer clic en "Enable"

## 2. Crear Credenciales OAuth
1. APIs & Services > Credentials
2. "Create Credentials" > "OAuth client ID"
3. Application type: "Desktop application"
4. Name: "Clawdbot Calendar"
5. Descargar el JSON de credenciales

## 3. Scopes necesarios
- `https://www.googleapis.com/auth/calendar.readonly` (para leer eventos)
- `https://www.googleapis.com/auth/calendar.events.readonly` (alternativa más restrictiva)

## 4. Test OAuth flow
- Primera vez necesita autorización en browser
- Después se guarda refresh token

## Next steps
- Instalar google-auth + googleapis en el skill
- Crear script de autenticación
- Integrar con heartbeat system