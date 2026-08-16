from dataclasses import dataclass
from enum import Enum

# all Priority_Report
class ReportPriority(Enum):
    CRITICAL = "Critical"
    UNKNOWN= "Unknown"   # when user does not enter the priority
    MEDIUM = "Medium"
    HIGH = "High"
    LOW = "Low"


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
    EXPERIENCE = "Experience"
    EXPERIENCE_DESCRIPTION = "EperienceDescription"
    EXPERIENCE_CATEGORY = "ExperienceCategory"
    EXPERIENCE_TITLE = "ExperienceTitle"

    def is_report(self):
        """ this function retruns true when user wants Submit Report

        Returns: 
            Boolian : True/False
        """

        return self.value.startswith(self.REPORT.value)
    
    def is_experience(self):
            """ this function retruns true when user wants Submit Experience
    
            Returns: 
                Boolian : True/False
            """
    
            return self.value.startswith(self.EXPERIENCE.value)
    
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
