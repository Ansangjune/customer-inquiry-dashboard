"""Customer inquiry summary response schemas."""

from pydantic import BaseModel, Field


class StatusBreakdown(BaseModel):
    """Inquiry counts grouped by lifecycle status."""

    open: int = Field(ge=0, description="Inquiries that have not been picked up yet")
    in_progress: int = Field(ge=0, description="Inquiries currently being handled")
    resolved: int = Field(ge=0, description="Inquiries marked as resolved")
    closed: int = Field(ge=0, description="Inquiries closed without further action")


class CategoryCount(BaseModel):
    """Inquiry count for a single category."""

    category: str = Field(description="Inquiry category label, e.g. 'billing'")
    count: int = Field(ge=0, description="Number of inquiries in this category")


class RecentInquiry(BaseModel):
    """Lightweight view of a recent inquiry for the dashboard list."""

    id: str = Field(description="Inquiry identifier")
    customer: str = Field(description="Customer display name")
    subject: str = Field(description="Short subject line of the inquiry")
    status: str = Field(description="Current lifecycle status")
    category: str = Field(description="Inquiry category label")
    created_at: str = Field(description="ISO-8601 timestamp of when the inquiry was opened")


class InquiriesSummary(BaseModel):
    """Aggregate summary used by the customer inquiry dashboard landing view."""

    total: int = Field(ge=0, description="Total number of inquiries on record")
    today: int = Field(ge=0, description="Inquiries opened today")
    last_7_days: int = Field(ge=0, description="Inquiries opened in the last 7 days")
    by_status: StatusBreakdown = Field(description="Breakdown of inquiries by status")
    by_category: list[CategoryCount] = Field(description="Breakdown of inquiries by category")
    recent: list[RecentInquiry] = Field(description="Most recent inquiries (newest first)")
