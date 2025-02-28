# Giji - Herramientas de Desarrollo

Colección de herramientas para optimizar el flujo de desarrollo:
- 🤖 Commits inteligentes con IA
- 📝 Generación de PRs con descripción automática
- 🎫 Integración con Jira
- 🔔 Integración con Slack

## Instalación

```bash
pip install giji
```

## Configuración

### Configurar Gemini (Requerido)
```bash
export GEMINI_API_KEY='your-api-key'
```

### Configurar Jira (Opcional)
```bash
export JIRA_SERVER_URL='https://your-domain.atlassian.net'
export JIRA_EMAIL='your.email@company.com'
export JIRA_TOKEN='your-api-token'
```

### Configurar Slack (Opcional)
Para recibir notificaciones en Slack, necesitas configurar un Incoming Webhook:

1. Ve a tu Slack workspace en el navegador
2. Haz click en el nombre del canal donde quieres recibir las notificaciones
3. En el menú del canal, selecciona "Configuración > Integraciones"
4. Click en "Añadir una aplicación"
5. Busca y selecciona "Incoming WebHooks"
6. Click en "Añadir a Slack"
7. Elige el canal y click en "Añadir integración"
8. Copia el Webhook URL y configúralo:
```bash
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/XXX/YYY/ZZZ'
```

Para verificar tu configuración:
```bash
giji config        # Verificar toda la configuración
giji config -t slack  # Verificar solo configuración de Slack
```

## Comandos

### Pull Requests

Crear un PR con descripción generada por IA:
```bash
# PR básico
giji pr -b main

# PR como borrador
giji pr -b main -d

# PR con ticket Jira
giji pr -b main -t SIS-123

# PR sin auto-commit
giji pr -b main -n

# PR con notificación a Slack
giji pr -b main -s

# PR con notificación a Slack y mensaje personalizado
giji pr -b main -s -m "Por favor revisar los cambios en el componente X"

# PR completo con todas las integraciones
giji pr -b main -s -m "Listo para review" -t SIS-123 -c -d
```

Opciones disponibles:
- `-b, --base`: Rama base (default: master)
- `-t, --ticket`: Número de ticket JIRA
- `-d, --draft`: Crear PR como borrador
- `-n, --no-commit`: No hacer commit automático
- `-c, --comment`: Agregar comentario en Jira
- `-s, --slack`: Enviar notificación a Slack
- `-m, --message`: Mensaje adicional para la notificación de Slack

### Slack

Enviar mensajes directamente a Slack:
```bash
# Mensaje simple
giji slack send "Hola equipo!"

# Mensaje con emojis
giji slack send "Deploy completado ✅"

# Mensaje con múltiples líneas
giji slack send "🚀 Nueva versión desplegada
• Feature 1
• Feature 2"
```

## Notificaciones de Slack

Las notificaciones de PR en Slack incluyen:
- URL del Pull Request
- Número de ticket Jira (con enlace directo)
- Mensaje personalizado (opcional)

Ejemplo de notificación:
```
🎉 *Nuevo Pull Request creado*
• *URL:* https://github.com/...
• *Ticket:* SIS-123 (enlace a Jira)
💬 *Mensaje:* Por favor revisar los cambios en el componente X
```

## Ejemplos y Ayuda

Ver ejemplos detallados:
```bash
giji examples
```

Ver ayuda de cualquier comando:
```bash
giji --help
giji pr --help
giji slack --help
```

## Requisitos

- Python 3.7+
- Git
- GitHub CLI (`gh`)
- API key de Gemini
- Credenciales de Jira (para funcionalidades de Jira)

## Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.


## Soporte

Si encuentras algún problema o tienes una sugerencia, por favor crea un issue en el [repositorio de GitHub](https://github.com/cometa/giji/issues).
