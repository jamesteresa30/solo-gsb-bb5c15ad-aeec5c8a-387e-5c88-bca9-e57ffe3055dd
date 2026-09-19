"""API 请求模型。"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TextIn(BaseModel):
    text: str = Field(default="", description="批量录入文本")


class ConfigIn(BaseModel):
    transfer_minutes: int = Field(gt=0, description="换乘有效间隔（分钟）")
    transfer_discount: float = Field(ge=0, description="换乘抵扣额（元）")
    daily_cap: float = Field(ge=0, description="每卡每运营日封顶额（元）")
    day_split_hour: int = Field(ge=0, le=23, description="运营日分界时刻")


class TrialConfigIn(BaseModel):
    """规则试算对比的草案参数。

    不在此处做数值约束：非法草案应走 core.validate_config，
    返回与正式核验一致的 CONFIG_BAD 定位错误（HTTP 422）。
    """
    transfer_minutes: float = Field(description="草案：换乘有效间隔（分钟）")
    transfer_discount: float = Field(description="草案：换乘抵扣额（元）")
    daily_cap: float = Field(description="草案：每卡每运营日封顶额（元）")
    day_split_hour: float = Field(description="草案：运营日分界时刻（0-23）")


class GatePeakAuditIn(BaseModel):
    """站点闸机峰值审计参数。

    window_minutes 在请求层约束为 1～120 的整数；核心层再做一次
    校验（返回 CONFIG_BAD），保证直接调用 core 时非法值也被拦截。
    min_alert_count 留空（null）表示不设置最低告警数，所有分组均
    不标记 alert；填写时必须为 ≥1 的整数。
    """
    window_minutes: int = Field(ge=1, le=120,
                                description="峰值窗口长度（分钟），1～120")
    min_alert_count: Optional[int] = Field(
        default=None, ge=1,
        description="最低告警数；峰值刷卡数达到该值的分组才标记告警")
