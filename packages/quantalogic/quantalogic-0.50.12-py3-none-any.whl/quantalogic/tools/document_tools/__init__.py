"""
Document Tools Module

This module provides optional tools for converting markdown to various document formats.
"""

from typing import Any
import importlib
import logging

logger = logging.getLogger(__name__)

# List of available tools for introspection
__all__ = [
    'markdown_to_docx_tool',
    'markdown_to_epub_tool', 
    'markdown_to_html_tool',
    'markdown_to_ipynb_tool',
    'markdown_to_latex_tool',
    'markdown_to_pdf_tool',
    'markdown_to_pptx_tool'
]

def __getattr__(name: str) -> Any:
    """
    Dynamically import optional tools with graceful error handling.
    
    Args:
        name (str): Name of the tool to import
    
    Returns:
        Any: Imported tool or None if import fails
    """
    try:
        module = importlib.import_module(f'.{name}', package='quantalogic.tools.document_tools')
        return getattr(module, name)
    except (ImportError, AttributeError) as e:
        logger.warning(f"Optional tool {name} could not be imported: {e}")
        return None
