from dataclasses import dataclass
from enum import Enum

# all Priority_Report
class ReportPriority(Enum):
    CRITICAL = "Critical"
    UNKNOWN= "Unknown"
    MEDIUM = "Medium"
    HIGH = "High"
    LOW = "Low"

    # when user does not enter the priority


class ReportCategory(Enum):
    BREAKDOWN = "Breakdown"
    OTHER = "Other"
    ERROR = "Error"
    BUG = "Bug"

# all User_stats
class UserState(Enum):
    NORMAL = "Normal"
    CHAT = "Chat"

    # Report stats
    REPORT = "Report"
    REPORT_DESCRIPTION = "ReportDescription"
    REPORT_CATEGORY = "ReportCategory"
    REPORT_PRIORITY = "ReportPriority"
    REPORT_TITLE = "ReportTitle"

    # Exprience stats
    EXPERIENCE = "Eperience"
    EXPERIENCE_DESCRIPTION = "EperienceDescription"
    EXPERIENCE_CATEGORY = "ExperienceCategory"
    EXPERIENCE_TITLE = "ExperienceTitle"

    def not_normal_or_chat(self):
        """ this function retruns true when user wants Submit Report or Experience

        Returns: 
            Boolian : True/False
        """
        return self.value.startswith("Report") or self.value.startswith("Experience")
    
class ExperienceCategory(Enum):
    INNOVATION = "Innovation"
    DEBUGING = "Debuging"
    OTHER = "Other"
    IDEA = "Idea"

@dataclass(slots=True)
class StepResult():
    message : str
    next_state : UserState
    finished : bool = True 
    keyboard : list | None = None 
    experience : bool = False 