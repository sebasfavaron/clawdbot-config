# Volver al Kiosk (backup y pasos)

## Backup ya creado
- Config anterior de nginx:
  - `/etc/nginx/sites-available/kiosk.bak`

## Pasos para volver al kiosk
1) Restaurar el config anterior:
```bash
sudo cp /etc/nginx/sites-available/kiosk.bak /etc/nginx/sites-available/kiosk
```

2) Validar configuración:
```bash
sudo nginx -t
```

3) Recargar nginx:
```bash
sudo systemctl reload nginx
```

## Opcional: restaurar contenido del kiosk
El config anterior apuntaba a:
- root: `/opt/player/current`
- videos: `/opt/player/videos/`
- health: `/opt/player/health.json`

Si esos paths siguen intactos, no hace falta tocar nada.

## Cómo volver al portal
```bash
sudo cp /etc/nginx/sites-available/kiosk.portal /etc/nginx/sites-available/kiosk
sudo nginx -t && sudo systemctl reload nginx
```

## Backup del portal
- Build actual: `/var/www/portal`
- Código: `/home/sebas/clawd/web/portal`
