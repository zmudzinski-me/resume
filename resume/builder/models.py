from dataclasses import dataclass
from datetime import date


@dataclass
class ExperienceCompanyRole:
    role_name: str
    start_date: date
    end_date: date | None


@dataclass
class ExperienceCompany:
    company_name: str
    roles: list[ExperienceCompanyRole]
