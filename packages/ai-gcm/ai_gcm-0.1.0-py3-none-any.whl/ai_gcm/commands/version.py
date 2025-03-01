"""Version command module."""

import click

@click.command()
def version():
    """
    Show the version of the application.
    
    This command displays the current version number of the AI Commit tool.
    Version information is hardcoded and should be updated with each release.

    Example:
        $ ai-gcm version
        v1.0.0
    """
    click.echo("v1.0.0") 
