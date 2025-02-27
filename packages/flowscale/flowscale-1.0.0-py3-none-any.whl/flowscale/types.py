from typing import List, Dict, Any, Optional, TypedDict

class ContainerStatus(TypedDict):
    container: str
    status: str

class HealthCheckResponse(TypedDict):
    status: str
    data: List[ContainerStatus]

class QueueItem(TypedDict):
    container: str
    queue: Dict[str, Any]

class QueueResponse(TypedDict):
    status: str
    data: List[QueueItem]

class ExecuteWorkflowResponseData(TypedDict):
    output_names: List[str]
    run_id: str

class ExecuteWorkflowResponse(TypedDict):
    status: str
    data: ExecuteWorkflowResponseData

class GetOutputResponseData(TypedDict):
    download_url: str
    generation_status: str

class GetOutputResponse(TypedDict):
    status: str
    data: GetOutputResponseData

class InputItem(TypedDict):
    path: str
    value: str
    s3_key: Optional[str]
    url: Optional[str]

class OutputItem(TypedDict):
    filename: str
    s3_key: Optional[str]
    url: Optional[str]

class RunDetail(TypedDict):
    _id: str
    team_id: str
    workflow_id: str
    group_id: Optional[str]
    status: str
    inputs: List[InputItem]
    outputs: List[OutputItem]
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]

class RunDetailResponse(TypedDict):
    status: str
    data: RunDetail

class RunListResponseData(TypedDict):
    group_id: str
    count: int
    runs: List[RunDetail]

class RunListResponse(TypedDict):
    status: str
    data: RunListResponseData

class CancelRunResponse(TypedDict):
    status: str
    data: str

class ErrorResponse(TypedDict):
    status: str
    errors: str