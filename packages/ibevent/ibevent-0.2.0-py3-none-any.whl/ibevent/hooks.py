"""Hook system for extending IBEvent functionality.

This module provides a flexible hook system that allows users to extend and customize
the behavior of the IBEvent framework without modifying its core code. It includes
utilities for loading, managing, and executing hook functions at various points in
the IBEvent lifecycle.

Key components:
- HookContext: A context object for sharing data between hooks.
- load_hook: Function to dynamically load a hook from a file.
- execute_hooks: Function to execute a list of hooks with a given context.

Typical usage example:

    from ibevent.hooks import HookContext, load_hook, execute_hooks

    # Create a hook context
    context = HookContext()

    # Define hook files
    hook_files = ['/path/to/hook1.py', '/path/to/hook2.py']

    # Load and execute hooks
    execute_hooks(hook_files, context)

    # Access shared data
    result = context.data.get('some_key')

Hook files should define a 'run' function that takes a HookContext object:

    # Example hook file: hook1.py
    def run(context):
        # Perform some action
        context.data['some_key'] = 'some_value'

This module is designed to be extensible, allowing users to add custom functionality
to various parts of the IBEvent system without altering the core implementation.
"""

import importlib.util
import os

from loguru import logger


class HookContext(object):
    """Context object for sharing data between hooks.

    This class provides a simple data sharing mechanism between hooks through
    its data dictionary attribute. Hooks can store and retrieve data using
    this context object.

    Attributes:
        data (dict): Dictionary for storing shared data between hooks.
    """

    def __init__(self):
        """Initialize an empty HookContext.

        The data dictionary is initialized as an empty dict and can be
        populated by hooks during execution.
        """
        self.data = {}


def load_hook(file_path):
    """Load a hook module from a file path and return its run function.

    This function dynamically loads a Python module from the given file path
    and extracts its 'run' function. The module should define a function
    named 'run' that takes a HookContext object as its argument.

    Args:
        file_path (str): Absolute path to the hook module file.

    Returns:
        callable: The run function from the module, or None if loading fails.

    Example:
        >>> hook = load_hook('/path/to/hook.py')
        >>> if hook:
        ...     hook(context)
    """
    try:
        spec = importlib.util.spec_from_file_location("hook", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.run
    except Exception as e:
        logger.error("Failed to load hook from %s: %s", file_path, str(e))
        return None


def execute_hooks(hook_files, context):
    """Execute a list of hook modules with the given context.

    This function processes a list of hook files, loading and executing each one
    in sequence. Each hook is executed in isolation, meaning that if one hook
    fails, it won't prevent other hooks from executing.

    Each hook module is expected to contain a single function named `run`
    which takes a HookContext as its argument. The context object allows
    hooks to share data between themselves.

    Args:
        hook_files (list[str]): List of absolute paths to the hook modules.
        context (HookContext): The context object to pass to the hooks.

    Example:
        >>> context = HookContext()
        >>> hook_files = ['/path/to/pre_launch.py', '/path/to/setup_env.py']
        >>> execute_hooks(hook_files, context)

    Note:
        - Hooks are executed in the order they appear in hook_files
        - Each hook's errors are caught and logged, not propagated
        - Non-existent hook files are silently skipped
    """
    for hook_file in hook_files:
        if os.path.exists(hook_file):
            hook = load_hook(hook_file)
            if hook:
                try:
                    hook(context)
                except Exception as e:
                    logger.error("Error executing hook %s: %s", hook_file, str(e))
