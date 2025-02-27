from enum import Enum


class FlowNodeStatus(Enum):
    """
    Enum class for flow step status
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
