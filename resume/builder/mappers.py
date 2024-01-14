import re
from abc import ABC, abstractmethod
from typing import Any


class AbstractMapper(ABC):
    @classmethod
    @abstractmethod
    def map(cls, data: list[str]) -> list[dict[str, Any]]:
        pass


class ExperienceMapper(AbstractMapper):
    COMPANY_REGEX = r"#{3} (.*)"
    JOB_REGEX = r"- `(\d{4}\.\d{2}) - (Present|\d{4}\.\d{2})` \*{2}(.*)\*{2}"
    RESPONSIBILITY_REGEX = r"\s+- (.*)"

    @classmethod
    def map(cls, data: list[str]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for line in data:
            if form := re.match(cls.COMPANY_REGEX, line):
                result.append({"company_name": form.group(1), "jobs": []})
            if form := re.match(cls.JOB_REGEX, line):
                result[-1]["jobs"].append(
                    {
                        "name": form.group(3),
                        "start_date": form.group(1),
                        "end_date": form.group(2),
                        "responsibilities": [],
                    }
                )
            if form := re.match(cls.RESPONSIBILITY_REGEX, line):
                result[-1]["jobs"][-1]["responsibilities"].append(form.group(1))

        return result


class EducationMapper(AbstractMapper):
    UNIVERSITY_REGEX = r"#{3} (.*)"
    DEGREE_REGEX = r"- `(\d{4}\.\d{2}) - (\d{4}\.\d{2})` (.*)"

    @classmethod
    def map(cls, data: list[str]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for line in data:
            if form := re.match(cls.UNIVERSITY_REGEX, line):
                result.append({"university_name": form.group(1), "degrees": []})
            if form := re.match(cls.DEGREE_REGEX, line):
                result[-1]["degrees"].append(
                    {
                        "name": form.group(3),
                        "start_date": form.group(1),
                        "end_date": form.group(2),
                    }
                )

        return result


class CertificationMapper(AbstractMapper):
    CERTIFICATE_REGEX = r"- `(\d{4}\.\d{2})` \[(.*)\].*"

    @classmethod
    def map(cls, data: list[str]) -> list[dict[str, Any]]:
        return [
            {"name": form.group(2), "date": form.group(1)}
            for certification in data
            if (form := re.match(cls.CERTIFICATE_REGEX, certification))
        ]


class ProjectsMapper(AbstractMapper):
    PROJECT_TYPE_REGEX = r"### (.*)"
    PROJECT_REGEX = r"- `(\d{4}\.\d{2}) - (Present|\d{4}\.\d{2})` (.*)"

    @classmethod
    def map(cls, data: list[str]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for line in data:
            if form := re.match(cls.PROJECT_TYPE_REGEX, line):
                project_type = form.group(1)
                result.append({"name": project_type, "projects": []})
            if form := re.match(cls.PROJECT_REGEX, line):
                result[-1]["projects"].append(
                    {
                        "name": form.group(3),
                        "start_date": form.group(1),
                        "end_date": form.group(2),
                    }
                )

        return result
