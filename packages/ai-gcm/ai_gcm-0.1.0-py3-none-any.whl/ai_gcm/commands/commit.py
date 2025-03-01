"""Commit command module."""

import click

from ai_gcm.core.utils import (
    check_model_availability,
    get_git_changes,
    get_git_status,
    stage_all_changes,
    commit_changes,
    get_code_summary,
    generate_commit_message,
)

# Default configuration
SUMMARY_MODEL = "qwen2.5-coder"
COMMIT_MODEL = "llama3.2"

@click.command()
@click.option('--summary-model', '-s', default=SUMMARY_MODEL,
              help='Model to use for code summary generation')
@click.option('--commit-model', '-c', default=COMMIT_MODEL,
              help='Model to use for commit message generation')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output including summary')
def commit(summary_model: str, commit_model: str, verbose: bool):
    """
    Generate a commit message from staged changes using AI.

    This command:
    1. Gets the git diff of staged changes
    2. Uses qwen2.5-coder to analyze and summarize the changes
    3. Uses llama3.2 to generate a commit message

    Example:
        $ git add .
        $ ai-gcm commit
        $ ai-gcm commit --verbose
        $ ai-gcm commit -s qwen2.5-coder -c llama3.2
    """
    # Check model availability
    for model in [summary_model, commit_model]:
        available, available_models = check_model_availability(model)
        if not available:
            click.echo(f"Model '{model}' is not available. Please run: ollama pull {model}")
            if available_models:
                click.echo("\nAvailable models:")
                for i, m in enumerate(available_models, 1):
                    click.echo(f"  {i}. {m}")
            return

    # Get git changes
    changes = get_git_changes()
    if 'error' in changes:
        click.echo(f"Error: {changes['error']}")
        return

    # Check for changes
    if not changes['staged']:
        if changes['unstaged']:
            # Show unstaged changes
            click.echo("\nUnstaged changes found:")
            click.echo("-" * 40)
            click.echo(get_git_status())
            click.echo("-" * 40)
            
            if click.confirm("\nWould you like to stage these changes?"):
                if not stage_all_changes():
                    click.echo("Error staging changes")
                    return
                # Refresh changes
                changes = get_git_changes()
            else:
                click.echo("No staged changes found. Use 'git add' to stage your changes.")
                return
        else:
            click.echo("No changes found to commit.")
            return

    # Generate summary
    click.echo(f"\nAnalyzing changes using {summary_model}...")
    summary, summary_success = get_code_summary(changes['staged'], summary_model)
    if not summary_success:
        click.echo(summary)
        return

    if verbose:
        click.echo("\nCode Changes Summary:")
        click.echo("-" * 40)
        click.echo(summary)
        click.echo("-" * 40)

    # Generate commit message
    click.echo(f"\nGenerating commit message using {commit_model}...")
    commit_message, commit_success = generate_commit_message(summary, commit_model)
    if not commit_success:
        click.echo(commit_message)
        return

    click.echo("\nSuggested Commit Message:")
    click.echo("-" * 40)
    click.echo(commit_message)
    click.echo("-" * 40)

    # Ask for confirmation and commit
    if click.confirm("\nWould you like to use this commit message?"):
        success, message = commit_changes(commit_message)
        click.echo(message)
    else:
        click.echo("Commit cancelled.") 
