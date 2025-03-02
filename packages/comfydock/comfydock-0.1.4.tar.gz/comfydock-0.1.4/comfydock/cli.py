import os
import sys
import json
import click
import signal
import logging
import webbrowser
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Import from your ComfyDock server package:
# Make sure to install comfydock_server==0.1.4 so these imports work:
from comfydock_server.server import ComfyDockServer
from comfydock_server.config import ServerConfig

# --------------------------------------------------
# Constants and defaults
# --------------------------------------------------

# The directory in the user's home folder to store config, DB, etc.
CONFIG_DIR = Path.home() / ".comfydock"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Defaults for config.json if it doesn't exist
DEFAULT_CONFIG = {
    "comfyui_path": str(Path.home()),
    "db_file_path": str(CONFIG_DIR / "environments.json"),
    "user_settings_file_path": str(CONFIG_DIR / "user.settings.json"),
    "frontend_container_name": "comfydock-frontend",
    "frontend_image": "akatzai/comfydock-frontend",
    "frontend_version": "0.1.3",
    "backend_host": "127.0.0.1",
    "backend_port": 5172,
    "frontend_container_port": 8000,
    "frontend_host_port": 8000,
    "allow_multiple_containers": False,
    "dockerhub_tags_url": "https://hub.docker.com/v2/namespaces/akatzai/repositories/comfydock-env/tags?page_size=100",
}

# Help text for each field (used in 'comfydock config')
CONFIG_FIELD_HELP = {
    "comfyui_path": "Default filesystem path to your local ComfyUI clone or desired location.",
    "db_file_path": "Where to store known Docker environments (JSON).",
    "user_settings_file_path": "Where to store user preferences for ComfyDock/ComfyUI.",
    "frontend_container_name": "Name for the Docker container that serves the ComfyUI frontend.",
    "frontend_image": "Docker image to pull for the frontend container.",
    "frontend_version": "Tag/version to pull for the frontend container image.",
    "backend_host": "Host/IP for the backend FastAPI server.",
    "backend_port": "TCP port for the backend FastAPI server.",
    "frontend_container_port": "TCP port inside the container for the frontend.",
    "frontend_host_port": "TCP port on your local machine that maps to the container port.",
    "allow_multiple_containers": "Whether to allow multiple ComfyUI containers to run at once.",
    "dockerhub_tags_url": "URL to the Docker Hub API endpoint for retrieving available tags.",
}

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def ensure_config_dir_and_file():
    """Ensure ~/.comfydock/ exists and has a config.json."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

def load_config():
    """Load config from ~/.comfydock/config.json, creating defaults if necessary."""
    ensure_config_dir_and_file()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg_data = json.load(f)

    # Fill in any missing fields with defaults
    updated = False
    for key, default_value in DEFAULT_CONFIG.items():
        if key not in cfg_data:
            cfg_data[key] = default_value
            updated = True

    # If we updated the config with new defaults, save it back
    if updated:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg_data, f, indent=4)

    return cfg_data

def save_config(data):
    """Save the updated config dictionary to ~/.comfydock/config.json."""
    ensure_config_dir_and_file()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def configure_logging():
    """
    Configure logging to write at INFO level to a rotating log file,
    rotating at ~20MB with up to 3 backups.
    """
    ensure_config_dir_and_file()
    
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove any existing handlers so we don't print to console
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    log_file_path = CONFIG_DIR / "comfydock.log"

    # Set up rotating file handler
    file_handler = RotatingFileHandler(
        filename=str(log_file_path),
        maxBytes=20 * 1024 * 1024,  # 20MB
        backupCount=3
    )
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    
    # Prevent logs from propagating to any higher-level logger (which might print to console)
    logger.propagate = False

    return logger

# --------------------------------------------------
# CLI Commands
# --------------------------------------------------

@click.group()
@click.version_option("0.1.4", prog_name="ComfyDock CLI")
def cli():
    """
    ComfyDock CLI - Manage ComfyUI Docker environments.

    Commands:
      up       Start the server (backend + frontend).
      down     Stop the server (backend + frontend).
      config   Manage or display config values.
    """
    pass


@cli.command()
@click.option("--backend", is_flag=True, help="Start only the backend server without the frontend")
def up(backend):
    """
    Start the ComfyDock server and the Docker-based frontend.

    This command loads configuration from ~/.comfydock/config.json (creating
    defaults if needed) and starts up both the FastAPI backend and the
    Docker frontend container.
    
    With --backend flag, only starts the backend server without the frontend.
    """
    logger = configure_logging()
    logger.info("Running 'comfydock up'...")

    cfg_data = load_config()
    server_config = ServerConfig(**cfg_data)

    # Create and start the server
    server = ComfyDockServer(server_config)
    
    if backend:
        logger.info("Starting ComfyDockServer (backend only)...")
        click.echo("Starting ComfyDockServer (backend only)...")
        server.start_backend()
        status_message = "ComfyDock backend is now running!"
    else:
        logger.info("Starting ComfyDockServer (backend + frontend)...")
        click.echo("Starting ComfyDockServer (backend + frontend)...")
        server.start()
        status_message = "ComfyDock is now running!"
        
        # Attempt to open the default browser automatically (only for full mode)
        try:
            webbrowser.open_new_tab(f"http://localhost:{server_config.frontend_host_port}")
        except:
            pass

    # Print a nicely formatted message for the user
    click.secho("\n" + "=" * 60, fg="cyan", bold=True)
    click.secho(f"  {status_message}", fg="green", bold=True)
    
    if not backend:
        click.secho(f"  Open your browser to:  http://localhost:{server_config.frontend_host_port}", fg="cyan")
    
    click.secho("  Press Ctrl+C here to stop the server at any time.", fg="yellow")
    click.secho("=" * 60 + "\n", fg="cyan", bold=True)

    try:
        signal.pause()  # Wait until the user hits Ctrl+C or server signals exit
    except (KeyboardInterrupt, SystemExit):
        logger.info("Keyboard interrupt or system exit caught. Stopping the server.")
        # Clear the previous console output message with a shutdown message
        click.secho("\n" + "=" * 60, fg="cyan", bold=True)
        click.secho("  ComfyDock is shutting down...", fg="yellow", bold=True)
        click.secho("=" * 60 + "\n", fg="cyan", bold=True)
        server.stop()
        click.echo("Server has been stopped.")


@cli.command()
def down():
    """
    Stop the running ComfyDock server (backend + frontend).
    
    If you started the server in another terminal, calling 'down' here attempts
    to stop the same environment.
    """
    logger = configure_logging()
    logger.info("Running 'comfydock down'...")

    cfg_data = load_config()
    server_config = ServerConfig(**cfg_data)
    server = ComfyDockServer(server_config)

    logger.info("Stopping ComfyDockServer (backend + frontend)...")
    server.stop()
    click.echo("Server has been stopped.")


@cli.command()
@click.option("--list", "list_config", is_flag=True,
              help="List the current configuration values.")
@click.argument("field", required=False)
@click.argument("value", required=False)
def config(list_config, field, value):
    """
    Manage or display ComfyDock config values.

    - Without arguments, will prompt you interactively to edit each field.
    - With --list, simply displays the current config.
    - With FIELD VALUE, sets that config field to VALUE.

    Example:
      comfydock config comfyui_path /home/user/ComfyUI

    Fields you can set include:
      comfyui_path, db_file_path, user_settings_file_path,
      frontend_container_name, frontend_image, frontend_version,
      backend_host, backend_port, frontend_container_port,
      frontend_host_port, allow_multiple_containers,
      dockerhub_tags_url.
    """
    logger = configure_logging()
    logger.info("Running 'comfydock config'...")

    cfg_data = load_config()

    if list_config:
        click.echo("Current ComfyDock config:\n")
        for k, v in cfg_data.items():
            desc = CONFIG_FIELD_HELP.get(k, "")
            click.echo(f"  {k} = {v}")
            if desc:
                click.echo(f"     -> {desc}")
        return

    # If a user specified a field and value: set it directly
    if field and value:
        if field not in DEFAULT_CONFIG:
            click.echo(f"Warning: '{field}' is not a recognized config field.")
        cfg_data[field] = _convert_value(value)
        save_config(cfg_data)
        click.echo(f"Set '{field}' to '{value}' in {CONFIG_FILE}")
        return

    # Otherwise, do a short interactive update on all known fields
    for k in DEFAULT_CONFIG.keys():
        current_val = cfg_data.get(k, "")
        desc = CONFIG_FIELD_HELP.get(k, "")
        if desc:
            click.echo(f"\n{desc}")
        new_val = click.prompt(f"{k}", default=str(current_val))
        cfg_data[k] = _convert_value(new_val)

    save_config(cfg_data)
    click.echo("\nConfiguration updated successfully!")

def _convert_value(val):
    """
    A helper to convert user CLI input from strings to bools/ints if needed.
    Minimal example that tries bool/int, otherwise returns str.
    """
    # Try boolean
    if val.lower() in ["true", "false"]:
        return val.lower() == "true"

    # Try integer
    try:
        return int(val)
    except ValueError:
        pass

    # Fallback to string
    return val

def main():
    """
    The main entry point for the CLI.

    If packaging this into a module, you can
    set up a console_scripts entry point in your setup to call this.
    """
    cli()

if __name__ == "__main__":
    main()
