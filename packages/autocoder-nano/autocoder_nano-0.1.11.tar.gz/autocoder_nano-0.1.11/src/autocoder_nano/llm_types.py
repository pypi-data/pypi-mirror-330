import dataclasses
from enum import Enum
from typing import List, Dict, Any, Optional, Union, Tuple, Set

from pydantic import BaseModel, Field


class AutoCoderArgs(BaseModel):
    request_id: Optional[str] = None  #
    file: Optional[str] = ''  #
    source_dir: Optional[str] = None  # 项目的路径
    git_url: Optional[str] = None  #
    target_file: Optional[str] = None  # 用于存储 提示词/生成代码 或其他信息的目标文件
    query: Optional[str] = None  # 你想让模型做什么
    template: Optional[str] = 'common'  #
    project_type: Optional[str] = None  # 项目的类型
    index_build_workers: Optional[int] = 1  # 构建索引的线程数量
    index_filter_level: Optional[int] = 0  # 用于查找相关文件的过滤级别
    index_filter_file_num: Optional[int] = -1  #
    index_filter_workers: Optional[int] = 1  # 过滤文件的线程数量
    filter_batch_size: Optional[int] = 5  #
    anti_quota_limit: Optional[int] = 1  # 请求模型时的间隔时间(s)
    skip_build_index: Optional[bool] = False  # 是否跳过索引构建(索引可以帮助您通过查询找到相关文件)
    skip_filter_index: Optional[bool] = False  #
    verify_file_relevance_score: Optional[int] = 6  #
    auto_merge: Optional[Union[bool, str]] = False  # 自动合并代码 True or False, 'editblock'
    enable_multi_round_generate: Optional[bool] = False  # 启用多轮生成
    editblock_similarity: Optional[float] = 0.9  # 编辑块相似性
    execute: Optional[bool] = None  # 模型是否生成代码
    context: Optional[str] = None  #
    human_as_model: Optional[bool] = False  #
    human_model_num: Optional[int] = 1  #
    include_project_structure: Optional[bool] = False  #
    urls: Optional[Union[str, List[str]]] = ""  # 一些文档的URL/路径，可以帮助模型了解你当前的工作
    model: Optional[str] = ""  # 您要驱动运行的模型
    model_max_input_length: Optional[int] = 6000  # 模型最大输入长度
    skip_confirm: Optional[bool] = False
    silence: Optional[bool] = False
    current_chat_model: Optional[str] = ""
    current_code_model: Optional[str] = ""

    # RAG 相关参数
    rag_url: Optional[str] = ""
    rag_doc_filter_relevance: int = 6  # 文档过滤相关性阈值,高于该值才会被认为高度相关
    rag_context_window_limit: Optional[int] = 30000  # RAG上下文窗口大小 120k 60k 30k
    full_text_ratio: Optional[float] = 0.7
    segment_ratio: Optional[float] = 0.2
    buff_ratio: Optional[float] = 0.1
    required_exts: Optional[str] = None    # 指定处理的文件后缀,例如.pdf,.doc
    monitor_mode: bool = False  # 监控模式,会监控doc_dir目录中的文件变化
    enable_hybrid_index: bool = False  # 开启混合索引
    disable_auto_window: bool = False
    hybrid_index_max_output_tokens: Optional[int] = 1000000
    rag_type: Optional[str] = "simple"
    tokenizer_path: Optional[str] = None
    enable_rag_search: Optional[Union[bool, str]] = False
    enable_rag_context: Optional[Union[bool, str]] = False
    disable_segment_reorder: bool = False
    disable_inference_enhance: bool = False

    # Git 相关参数
    skip_commit: Optional[bool] = False

    class Config:
        protected_namespaces = ()


class ServerArgs(BaseModel):
    host: str = None
    port: int = 8000
    uvicorn_log_level: str = "info"
    allow_credentials: bool = False
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    ssl_keyfile: str = None
    ssl_certfile: str = None
    response_role: str = "assistant"
    doc_dir: str = ""
    tokenizer_path: Optional[str] = None


class SourceCode(BaseModel):
    module_name: str
    source_code: str
    tag: str = ""
    tokens: int = -1
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LLMRequest(BaseModel):
    model: str  # 指定使用的语言模型名称
    messages: List[Dict[str, str]]  # 包含对话消息的列表，每个消息是一个字典，包含 "role"（角色）和 "content"（内容）
    stream: bool = False  # 是否以流式方式返回响应，默认为 False
    max_tokens: Optional[int] = None  # 生成的最大 token 数量，如果未指定，则使用模型默认值
    temperature: Optional[float] = None  # 控制生成文本的随机性，值越高生成的内容越随机，默认为模型默认值
    top_p: Optional[float] = None  # 控制生成文本的多样性，值越高生成的内容越多样，默认为模型默认值
    n: Optional[int] = None  # 生成多少个独立的响应，默认为 1
    stop: Optional[List[str]] = None  # 指定生成文本的停止条件，当生成的内容包含这些字符串时停止生成
    presence_penalty: Optional[float] = None  # 控制生成文本中是否鼓励引入新主题，值越高越鼓励新主题，默认为 0
    frequency_penalty: Optional[float] = None  # 控制生成文本中是否减少重复内容，值越高越减少重复，默认为 0


class LLMResponse(BaseModel):
    output: Union[str, List[float]] = ''  # 模型的输出，可以是字符串或浮点数列表
    input: Union[str, Dict[str, Any]] = ''  # 模型的输入，可以是字符串或字典
    metadata: Dict[str, Any] = dataclasses.field(
        default_factory=dict  # 元数据，包含与响应相关的额外信息，默认为空字典
    )


class IndexItem(BaseModel):
    module_name: str
    symbols: str
    last_modified: float
    md5: str  # 新增文件内容的MD5哈希值字段


class TargetFile(BaseModel):
    file_path: str
    reason: str = Field(
        ..., description="The reason why the file is the target file"
    )


class FileList(BaseModel):
    file_list: List[TargetFile]


class SymbolType(Enum):
    USAGE = "usage"
    FUNCTIONS = "functions"
    VARIABLES = "variables"
    CLASSES = "classes"
    IMPORT_STATEMENTS = "import_statements"


class SymbolsInfo(BaseModel):
    usage: Optional[str] = Field('', description="用途")
    functions: List[str] = Field([], description="函数")
    variables: List[str] = Field([], description="变量")
    classes: List[str] = Field([], description="类")
    import_statements: List[str] = Field([], description="导入语句")


class VerifyFileRelevance(BaseModel):
    relevant_score: int
    reason: str


class CodeGenerateResult(BaseModel):
    contents: List[str]
    conversations: List[List[Dict[str, Any]]]


class PathAndCode(BaseModel):
    path: str
    content: str


class RankResult(BaseModel):
    rank_result: List[int]


class MergeCodeWithoutEffect(BaseModel):
    success_blocks: List[Tuple[str, str]]
    failed_blocks: List[Any]


class CommitResult(BaseModel):
    success: bool
    commit_message: Optional[str] = None
    commit_hash: Optional[str] = None
    changed_files: Optional[List[str]] = None
    diffs: Optional[dict] = None
    error_message: Optional[str] = None


class Tag(BaseModel):
    start_tag: str
    content: str
    end_tag: str


class SymbolItem(BaseModel):
    symbol_name: str
    symbol_type: SymbolType
    file_name: str


class VariableHolder:
    TOKENIZER_PATH = None
    TOKENIZER_MODEL = None


class DeleteEvent(BaseModel):
    file_paths: Set[str]


class AddOrUpdateEvent(BaseModel):
    file_infos: List[Tuple[str, str, float, str]]


class DocRelevance(BaseModel):
    is_relevant: bool
    relevant_score: int


class TaskTiming(BaseModel):
    submit_time: float = 0
    end_time: float = 0
    duration: float = 0
    real_start_time: float = 0
    real_end_time: float = 0
    real_duration: float = 0


class FilterDoc(BaseModel):
    source_code: SourceCode
    relevance: DocRelevance
    task_timing: TaskTiming


class RagConfig(BaseModel):
    filter_config: Optional[str] = None
    answer_config: Optional[str] = None