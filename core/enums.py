from dataclasses import dataclass
from enum import Enum

# all Priority_Report
class ReportPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    # when user does not enter the priority
    UNKNOWN = "Unknown"

class Category(Enum):
    EXPERIENCE = "Experience"
    BREAKDOWN = "Breakdown"
    IDEA = "Idea"
    OTHER = "Other"
    
# all User_stats
class UserState(Enum):
    NORMAL = "Normal"
    CHAT = "Chat"
    # Report stats
    REPORT_DESCRIPTION = "ReportDescription"
    REPORT_TITLE = "ReportTitle"
    REPORT_CATEGORY = "ReportCategory"
    REPORT_PRIORITY = "ReportPriority"

    def is_report(self):
        """ this function retruns true when user wants Submit Report

        Returns:
            Boolian : True/False
        """
        return self.value.startswith("Report")

@dataclass(slots=True)
class StepResult():
    message : str
    next_state : UserState
    finished : bool = True 
    keyboard : list | None = None 