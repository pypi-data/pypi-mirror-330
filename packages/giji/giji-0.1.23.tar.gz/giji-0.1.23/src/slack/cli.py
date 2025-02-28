import typer
from rich import print
from rich.console import Console
from .client import SlackClient

# Create Slack CLI group
app = typer.Typer(
    name="slack",
    help="🔔 Comandos de Slack",
    no_args_is_help=True,
)

console = Console()


@app.command(
    name="send",
    help="Envía un mensaje a Slack",
    short_help="Envía mensaje a Slack",
)
def send_message(
    message: str = typer.Argument(
        ...,
        help="Mensaje a enviar",
    ),
):
    """
    Envía un mensaje al canal de Slack configurado.

    Ejemplos:
      giji slack send "Hola equipo!"
      giji slack send "Deploy completado ✅"
    """
    try:
        slack = SlackClient.from_env()
        if slack.send_message(message):
            print("[green]✨ Mensaje enviado exitosamente a Slack[/green]")
        else:
            print("[red]❌ No se pudo enviar el mensaje a Slack[/red]")
            raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1) 