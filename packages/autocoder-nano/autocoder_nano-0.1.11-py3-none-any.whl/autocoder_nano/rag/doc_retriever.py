from abc import ABC, abstractmethod
from typing import Generator, Optional, Dict, Any, List, Tuple
from uuid import uuid4

from loguru import logger

from autocoder_nano.llm_types import SourceCode
from autocoder_nano.rag.doc_cache import AutoCoderRAGAsyncUpdateQueue


class BaseDocumentRetriever(ABC):
    """Abstract base class for document retrieval."""
    @abstractmethod
    def get_cache(self, options: Optional[Dict[str, Any]] = None):
        """Get cached documents."""
        pass

    @abstractmethod
    def retrieve_documents(self, options: Optional[Dict[str, Any]] = None) -> Generator[SourceCode, None, None]:
        """Retrieve documents."""
        pass


class LocalDocumentRetriever(BaseDocumentRetriever):
    """Local filesystem document retriever implementation."""
    def __init__(
        self, path: str, ignore_spec, required_exts: list, on_ray: bool = False, monitor_mode: bool = False,
        single_file_token_limit: int = 60000, disable_auto_window: bool = False, enable_hybrid_index: bool = False
    ) -> None:
        self.path = path
        self.ignore_spec = ignore_spec
        self.required_exts = required_exts
        self.on_ray = on_ray
        self.monitor_mode = monitor_mode
        self.enable_hybrid_index = enable_hybrid_index
        self.single_file_token_limit = single_file_token_limit
        self.disable_auto_window = disable_auto_window

        # 多小的文件会被合并
        self.small_file_token_limit = self.single_file_token_limit / 4
        # 合并后的最大文件大小
        self.small_file_merge_limit = self.single_file_token_limit / 2

        if self.enable_hybrid_index:
            pass
            # self.cacher = AutoCoderRAGStorageCache(path, ignore_spec, required_exts, extra_params)
        else:
            if self.monitor_mode:
                pass
                # self.cacher = AutoCoderRAGDocListener(path, ignore_spec, required_exts)
            else:
                self.cacher = AutoCoderRAGAsyncUpdateQueue(path, ignore_spec, self.required_exts)

        logger.info(f"文档检索初始化完成，配置如下：")
        logger.info(f"  路径: {self.path}")
        logger.info(f"  禁用自动窗口: {self.disable_auto_window} ")
        logger.info(f"  单文件 token 限制: {self.single_file_token_limit}")
        logger.info(f"  小文件 token 限制: {self.small_file_token_limit}")
        logger.info(f"  小文件合并限制: {self.small_file_merge_limit}")
        logger.info(f"  启用混合索引: {self.enable_hybrid_index}")

    def get_cache(self, options: Optional[Dict[str, Any]] = None):
        return self.cacher.get_cache(options=options)

    def retrieve_documents(self, options: Optional[Dict[str, Any]] = None) -> Generator[SourceCode, None, None]:
        logger.info("文档检索开始. ")
        waiting_list = []
        waiting_tokens = 0
        for _, data in self.get_cache(options=options).items():
            for source_code in data["content"]:
                doc = SourceCode.model_validate(source_code)
                if self.disable_auto_window:
                    yield doc
                else:
                    if doc.tokens <= 0:  # 空文件
                        yield doc
                    elif doc.tokens < self.small_file_token_limit:
                        waiting_list, waiting_tokens = self._add_to_waiting_list(doc, waiting_list, waiting_tokens)
                        if waiting_tokens >= self.small_file_merge_limit:
                            yield from self._process_waiting_list(waiting_list)
                            waiting_list = []
                            waiting_tokens = 0
                    elif doc.tokens > self.single_file_token_limit:
                        yield from self._split_large_document(doc)
                    else:
                        yield doc
        if waiting_list and not self.disable_auto_window:
            yield from self._process_waiting_list(waiting_list)
        logger.info("文档检索完成. ")

    @staticmethod
    def _add_to_waiting_list(
            doc: SourceCode, waiting_list: List[SourceCode], waiting_tokens: int
    ) -> Tuple[List[SourceCode], int]:
        waiting_list.append(doc)
        return waiting_list, waiting_tokens + doc.tokens

    def _process_waiting_list(self, waiting_list: List[SourceCode]) -> Generator[SourceCode, None, None]:
        if len(waiting_list) == 1:
            yield waiting_list[0]
        elif len(waiting_list) > 1:
            yield self._merge_documents(waiting_list)

    @staticmethod
    def _merge_documents(docs: List[SourceCode]) -> SourceCode:
        merged_content = "\n".join(
            [f"#File: {doc.module_name}\n{doc.source_code}" for doc in docs]
        )
        merged_tokens = sum([doc.tokens for doc in docs])
        merged_name = f"Merged_{len(docs)}_docs_{str(uuid4())}"
        logger.info(f"已将 {len(docs)} 个文档合并为 {merged_name}(tokens 数：{merged_tokens})")
        return SourceCode(
            module_name=merged_name,
            source_code=merged_content,
            tokens=merged_tokens,
            metadata={"original_docs": [doc.module_name for doc in docs]},
        )

    def _split_large_document(self, doc: SourceCode) -> Generator[SourceCode, None, None]:
        chunk_size = self.single_file_token_limit
        total_chunks = (doc.tokens + chunk_size - 1) // chunk_size
        logger.info(f"正在将文档 {doc.module_name} 拆分为 {total_chunks} 个块")
        for i in range(0, doc.tokens, chunk_size):
            chunk_content = doc.source_code[i: i + chunk_size]
            chunk_tokens = min(chunk_size, doc.tokens - i)
            chunk_name = f"{doc.module_name}#chunk{i // chunk_size + 1}"
            logger.debug(f"  Created chunk: {chunk_name} (tokens: {chunk_tokens})")
            yield SourceCode(
                module_name=chunk_name,
                source_code=chunk_content,
                tokens=chunk_tokens,
                metadata={
                    "original_doc": doc.module_name,
                    "chunk_index": i // chunk_size + 1,
                },
            )