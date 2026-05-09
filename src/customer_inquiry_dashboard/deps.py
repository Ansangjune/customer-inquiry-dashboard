"""Reusable FastAPI Depends helpers."""

from typing import Annotated

from fastapi import Depends

from customer_inquiry_dashboard.settings import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]
