"""Errors the tools raise. Catch ToolError to handle any of them."""


class ToolError(Exception):
    """Base class for every error the tools raise on purpose."""


class BuildError(ToolError):
    """The build found a problem with its input or its output and stopped before writing."""


class HarnessError(ToolError):
    """The `claude` or `opencode` CLI failed, which says nothing about the skill."""
