from dataclasses import dataclass

# all Priority_Report
class ReportPriority:
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

# all User_stats
class UserState:

    NORMAL = "Normal"
    CHAT = "Chat"
    REPORT_DESCRIPTION = "ReportDescription"
    REPORT_TITLE = "ReportTitle"
    REPORT_CATEGORY = "ReportCategory"
    REPORT_PRIORITY = "ReportPriority"


@dataclass(slots=True)
class step_resualts():
    message : str
    next_state : str
    finished : bool = True 