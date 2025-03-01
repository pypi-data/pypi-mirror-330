"""Tools for the QuantaLogic agent."""

import importlib
import sys
from typing import Any, Dict


class LazyLoader:
    """
    Lazily import a module only when its attributes are accessed.
    This helps reduce startup time by deferring imports until needed.
    """
    def __init__(self, module_path: str, optional: bool = False):
        self.module_path = module_path
        self._module = None
        self.optional = optional

    def __getattr__(self, name: str) -> Any:
        if self._module is None:
            try:
                self._module = importlib.import_module(self.module_path)
            except ImportError as e:
                if self.optional:
                    # If the tool is optional, log a warning but don't raise an error
                    print(f"Warning: Optional tool {self.module_path} could not be imported: {e}")
                    return None
                raise

        return getattr(self._module, name)


# Map of tool names to their import paths and optional status
_TOOL_IMPORTS = {
    "AgentTool": (".agent_tool", False),
    "ComposioTool": (".composio.composio", False),
    "GenerateDatabaseReportTool": (".database.generate_database_report_tool", False),
    "SQLQueryToolAdvanced": (".database.sql_query_tool_advanced", False),
    "MarkdownToDocxTool": (".document_tools.markdown_to_docx_tool", True),
    "MarkdownToEpubTool": (".document_tools.markdown_to_epub_tool", True),
    "MarkdownToHtmlTool": (".document_tools.markdown_to_html_tool", True),
    "MarkdownToIpynbTool": (".document_tools.markdown_to_ipynb_tool", True),
    "MarkdownToLatexTool": (".document_tools.markdown_to_latex_tool", True),
    "MarkdownToPdfTool": (".document_tools.markdown_to_pdf_tool", True),
    "MarkdownToPptxTool": (".document_tools.markdown_to_pptx_tool", True),
    "DownloadHttpFileTool": (".download_http_file_tool", False),
    "DuckDuckGoSearchTool": (".duckduckgo_search_tool", False),
    "EditWholeContentTool": (".edit_whole_content_tool", False),
    "ElixirTool": (".elixir_tool", False),
    "ExecuteBashCommandTool": (".execute_bash_command_tool", False),
    "BitbucketCloneTool": (".git.bitbucket_clone_repo_tool", False),
    "BitbucketOperationsTool": (".git.bitbucket_operations_tool", False),
    "CloneRepoTool": (".git.clone_repo_tool", False),
    "GitOperationsTool": (".git.git_operations_tool", False),
    "GoogleNewsTool": (".google_packages.google_news_tool", False),
    "GrepAppTool": (".grep_app_tool", False),
    "LLMImageGenerationTool": (".image_generation.dalle_e", False),
    "InputQuestionTool": (".input_question_tool", False),
    "JinjaTool": (".jinja_tool", False),
    "ListDirectoryTool": (".list_directory_tool", False),
    "LLMTool": (".llm_tool", False),
    "LLMVisionTool": (".llm_vision_tool", False),
    "MarkitdownTool": (".markitdown_tool", False),
    "NasaApodTool": (".nasa_packages.nasa_apod_tool", False),
    "NasaNeoWsTool": (".nasa_packages.nasa_neows_tool", False),
    "NodeJsTool": (".nodejs_tool", False),
    "PresentationLLMTool": (".presentation_tools.presentation_llm_tool", False),
    "ProductHuntTool": (".product_hunt.product_hunt_tool", False),
    "PythonTool": (".python_tool", False),
    "RagTool": (".rag_tool.rag_tool", False),
    "ReadFileBlockTool": (".read_file_block_tool", False),
    "ReadFileTool": (".read_file_tool", False),
    "ReadHTMLTool": (".read_html_tool", False),
    "ReplaceInFileTool": (".replace_in_file_tool", False),
    "RipgrepTool": (".ripgrep_tool", False),
    "SafePythonInterpreterTool": (".safe_python_interpreter_tool", False),
    "SearchDefinitionNames": (".search_definition_names", False),
    "SequenceTool": (".sequence_tool", False),
    "SerpApiSearchTool": (".serpapi_search_tool", False),
    "SQLQueryTool": (".sql_query_tool", False),
    "TaskCompleteTool": (".task_complete_tool", False),
    "Tool": (".tool", False),
    "ToolArgument": (".tool", False),
    "UnifiedDiffTool": (".unified_diff_tool", False),
    "CSVProcessorTool": (".utilities.csv_processor_tool", False),
    "PrepareDownloadTool": (".utilities.download_file_tool", False),
    "MermaidValidatorTool": (".utilities.mermaid_validator_tool", False),
    "WikipediaSearchTool": (".wikipedia_search_tool", False),
    "WriteFileTool": (".write_file_tool", False),
}

# Create lazy loaders for each module path
_lazy_modules: Dict[str, LazyLoader] = {}
for tool, (path, optional) in _TOOL_IMPORTS.items():
    full_path = f"{__package__}{path}"
    if full_path not in _lazy_modules:
        _lazy_modules[full_path] = LazyLoader(full_path, optional)

# Set up attributes for lazy loading
_tools_to_lazy_modules = {}
for tool, (path, optional) in _TOOL_IMPORTS.items():
    full_path = f"{__package__}{path}"
    _tools_to_lazy_modules[tool] = _lazy_modules[full_path]

# Define __all__ so that import * works properly
__all__ = list(_TOOL_IMPORTS.keys())

# Set up lazy loading for each tool
for tool, lazy_module in _tools_to_lazy_modules.items():
    # This will create properties that lazily load the requested tool
    setattr(sys.modules[__name__], tool, getattr(lazy_module, tool))
