"""Utility functions for AI Commit."""

import json
import subprocess
from typing import Tuple, List, Dict

import ollama

from ai_gcm.core.models import CommitMessage

def get_available_models() -> List[str]:
    """
    Get list of available Ollama models.

    Returns:
        List[str]: List of available model names
    """
    try:
        models = ollama.list()
        return [m['name'] for m in models['models']]
    except Exception as e:
        return []

def check_model_availability(model: str) -> Tuple[bool, List[str]]:
    """
    Check if a model is available in Ollama.

    Args:
        model (str): The name of the model to check

    Returns:
        Tuple[bool, List[str]]: (is_available, available_models)
        - is_available: True if model is available, False otherwise
        - available_models: List of available model names
    """
    try:
        available_models = get_available_models()
        
        # Some models might have tags, so check both full name and base name
        model_base = model.split(':')[0]  # Handle cases like 'model:latest'
        
        is_available = any(
            m == model or m.startswith(f"{model_base}:")
            for m in available_models
        )
        
        return is_available, available_models
    except Exception:
        return False, []

def get_git_changes() -> Dict[str, str]:
    """
    Get both staged and unstaged git changes.

    Returns:
        Dict[str, str]: Dictionary containing:
        - 'staged': Staged changes diff
        - 'unstaged': Unstaged changes diff
    """
    try:
        # Get unstaged changes
        unstaged_diff = subprocess.run(
            ['git', 'diff'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get staged changes
        staged_diff = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            'staged': staged_diff.stdout.strip(),
            'unstaged': unstaged_diff.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        return {'error': str(e.stderr)}
    except Exception as e:
        return {'error': str(e)}

def get_git_status() -> str:
    """
    Get git status in short format.

    Returns:
        str: Git status output or error message
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return str(e.stderr)
    except Exception as e:
        return str(e)

def stage_all_changes() -> bool:
    """
    Stage all git changes.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.run(['git', 'add', '-A'], check=True)
        return True
    except Exception:
        return False

def commit_changes(message: str) -> Tuple[bool, str]:
    """
    Commit staged changes with the given message.

    Args:
        message (str): Commit message

    Returns:
        Tuple[bool, str]: (success, message)
        - success: True if commit was successful, False otherwise
        - message: Success or error message
    """
    try:
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            capture_output=True,
            text=True,
            check=True
        )
        return True, "Changes committed successfully!"
    except subprocess.CalledProcessError as e:
        return False, f"Error committing changes: {e.stderr}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_code_summary(diff: str, model: str) -> Tuple[str, bool]:
    """
    Get a summary of the code changes using the specified model.

    Args:
        diff (str): The git diff content
        model (str): The model to use for summarization

    Returns:
        Tuple[str, bool]: (summary, success)
        - summary: The generated summary or error message
        - success: True if successful, False otherwise
    """
    try:
        prompt = f"""Analyze this git diff and provide a concise summary of the changes:

{diff}

Provide a clear and specific summary of what changed. Focus on the important details."""

        response = ollama.generate(
            model=model,
            prompt=prompt,
            stream=False
        )
        
        return response['response'].strip(), True
    except Exception as e:
        return f"Error generating summary: {str(e)}", False

def generate_commit_message(summary: str, model: str) -> Tuple[str, bool]:
    """
    Generate a commit message based on the code summary.

    Args:
        summary (str): The code change summary
        model (str): The model to use for commit message generation

    Returns:
        Tuple[str, bool]: (commit_message, success)
        - commit_message: The generated commit message or error message
        - success: True if successful, False otherwise
    """
    try:
        prompt = f"""Based on this summary of code changes, generate a commit message following conventional commit format.

Summary of changes:
{summary}

Requirements for the commit message:
- Start with a verb in the present tense
- Be clear and specific
- Be under 72 characters for the first line
- Only include essential information
- Follow conventional commit format

Example commit types:
- feat: A new feature
- fix: A bug fix
- refactor: Code restructuring
- docs: Documentation changes
- style: Formatting changes
- test: Adding or updating tests
- chore: Maintenance tasks"""

        response = ollama.generate(
            model=model,
            prompt=prompt,
            format=CommitMessage.model_json_schema(),
            stream=False
        )
    
        # Parse the JSON string and validate using Pydantic
        try:
            # Parse the JSON string into a dictionary
            response_dict = json.loads(response['response'])
            commit_data = CommitMessage.model_validate(response_dict)
            return commit_data.message.strip(), True
        except json.JSONDecodeError as e:
            return f"Error parsing JSON response: {str(e)}", False
        except Exception as e:
            return f"Error validating commit message: {str(e)}", False
            
    except Exception as e:
        return f"Error generating commit message: {str(e)}", False 
