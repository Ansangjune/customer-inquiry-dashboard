"""Customer inquiry dashboard endpoints."""

from fastapi import APIRouter

from customer_inquiry_dashboard.schemas.inquiries import (
    CategoryCount,
    InquiriesSummary,
    RecentInquiry,
    StatusBreakdown,
)

router = APIRouter(prefix="/api/inquiries", tags=["inquiries"])


def _build_dummy_summary() -> InquiriesSummary:
    return InquiriesSummary(
        total=128,
        today=7,
        last_7_days=34,
        by_status=StatusBreakdown(open=21, in_progress=15, resolved=78, closed=14),
        by_category=[
            CategoryCount(category="billing", count=42),
            CategoryCount(category="technical", count=37),
            CategoryCount(category="account", count=28),
            CategoryCount(category="general", count=21),
        ],
        recent=[
            RecentInquiry(
                id="INQ-1042",
                customer="Lee Ji-won",
                subject="결제가 두 번 청구된 것 같아요",
                status="open",
                category="billing",
                created_at="2026-05-09T08:42:11Z",
            ),
            RecentInquiry(
                id="INQ-1041",
                customer="Kim Min-jae",
                subject="앱 로그인이 안돼요",
                status="in_progress",
                category="technical",
                created_at="2026-05-09T07:15:03Z",
            ),
            RecentInquiry(
                id="INQ-1040",
                customer="Park So-yeon",
                subject="비밀번호 재설정 메일이 안와요",
                status="resolved",
                category="account",
                created_at="2026-05-08T22:01:48Z",
            ),
            RecentInquiry(
                id="INQ-1039",
                customer="Choi Hyun-woo",
                subject="환불 절차 문의",
                status="open",
                category="billing",
                created_at="2026-05-08T18:33:20Z",
            ),
            RecentInquiry(
                id="INQ-1038",
                customer="Jung Eun-bi",
                subject="서비스 이용 가능 시간 문의",
                status="closed",
                category="general",
                created_at="2026-05-08T14:09:55Z",
            ),
        ],
    )


@router.get("/summary", response_model=InquiriesSummary)
async def get_inquiries_summary() -> InquiriesSummary:
    """Return aggregate inquiry metrics for the dashboard landing view."""
    return _build_dummy_summary()
