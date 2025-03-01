"""
llm-jina: LLM plugin for Jina AI
"""

__version__ = "0.3.0"

from .api import (
    jina_embed,
    jina_search,
    jina_read,
    jina_segment,
    jina_classify_text,
    jina_classify_images,
    jina_ground,
    jina_rerank,
    rerank_documents,
    jina_metaprompt_api,
    APIError,
)
from .commands import register_jina_commands

# Register our plugin commands
__llm_commands__ = register_jina_commands
