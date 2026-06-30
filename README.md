# Passenger MVP Tracker

Tracker visual del MVP Passenger — Kinetic / Pluralit.

## ¿Qué es esto?

Un Gantt interactivo que muestra el estado de avance del MVP de Passenger en tiempo real, basado en los issues del sprint activo de Jira (proyecto P224).

- **Actualización automática:** cada día hábil a las 7:45 AM (hora Argentina)
- **Datos:** directamente desde Jira — no hay datos manuales
- **Período:** 18 días hábiles · Jun 22 → Jul 17, 2026

## Cómo usar

Abrí el link que te compartió Pablo y listo. No hace falta login.

> Para ver la última actualización hacé clic en el nombre del proyecto o esperá al día siguiente.

## Setup (para el mantenedor)

### Primer setup

```bash
git clone https://github.com/[tu-usuario]/passenger-mvp-tracker
cd passenger-mvp-tracker
```

### Secrets necesarios (en GitHub → Settings → Secrets → Actions)

| Secret | Valor |
|--------|-------|
| `JIRA_EMAIL` | Tu email de Atlassian |
| `JIRA_TOKEN` | API token de https://id.atlassian.com/manage-profile/security/api-tokens |

### Correr manualmente

En GitHub → Actions → "Update Passenger MVP Tracker" → "Run workflow"

### GitHub Pages

Activar en Settings → Pages → Source: Deploy from branch → Branch: `main` → Folder: `/ (root)`
