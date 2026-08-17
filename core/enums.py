from dataclasses import dataclass
from enum import Enum

# all Priority_Report
class ReportPriority(Enum):
    CRITICAL = "critical"
    UNKNOWN= "unknown"   # when user does not enter the priority
    MEDIUM = "medium"
    HIGH = "high"
    LOW = "low"


class ReportCategory(Enum):
    BREAKDOWN = "breakdown"
    OTHER = "other"
    ERROR = "error"
    BUG = "bug"
    
# all User_stats
class UserState(Enum):
    NORMAL = "normal"
    CHAT = "chat"

    # Report stats
    REPORT = "report"
    REPORT_DESCRIPTION = "report_description"
    REPORT_CATEGORY = "report_category"
    REPORT_PRIORITY = "report_priority"
    REPORT_TITLE = "report_title"

    # Exprience stats
    EXPERIENCE = "experience"
    EXPERIENCE_DESCRIPTION = "experience_description"
    EXPERIENCE_CATEGORY = "experience_category"
    EXPERIENCE_TITLE = "experience_title"

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
    INNOVATION = "innovation"
    DEBUGING = "debuging"
    OTHER = "other"
    IDEA = "idea"

@dataclass(slots=True)
class StepResult():
    next_state : UserState
    finished : bool = True 
    experience : bool = False 
    keyboard : list | None = None
    error_code : str | None = None
    message : str | None = None 

@dataclass(slots=True)
class ValidatesOutput():
    status : bool = False
    message : str | None = None