from dataclasses import dataclass
from decimal import Decimal


@dataclass
class InvitroAnalyzeItem:
    city_href: str | None = None
    city_url: str | None = None
    city_name: str | None = None
    analysis_href: str | None = None
    analysis_url: str | None = None
    analysis_name: str | None = None
    description: str | None = None
    preparation: str | None = None
    purpose: str | None = None
    interpretation: str | None = None
    article_number: str | None = None
    total_price: str | Decimal | float | None = None


@dataclass
class InvitroCityItem:
    href: str | None = None
    url: str | None = None
    name: str | None = None
