from enum import Enum
from pydantic import BaseModel, Field


class UrgencyLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ActionCategory(str, Enum):
    BILLING = "Billing & Refunds"
    TECHNICAL = "Technical Support"
    GENERAL = "General Inquiry"
    COMPLAINT = "Customer Complaint"


class EmailAnalysis(BaseModel):
    """Pydantic model defining the required JSON structure for email analysis."""

    intent: str = Field(
        description="A concise summary of the primary goal of the email."
    )
    urgency: UrgencyLevel = Field(
        description="The priority level of the email based on customer emotion and business impact."
    )
    category: ActionCategory = Field(
        description="The operational category for routing the email."
    )
    summary: str = Field(
        description="A clear 1-2 sentence summary of the email content."
    )
    requires_human_followup: bool = Field(
        description="True if an agent must manually review/respond, False otherwise."
    )