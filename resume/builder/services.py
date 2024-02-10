import re
from typing import Any

import pdfkit
from jinja2 import Environment, FileSystemLoader

from builder.mappers import (
    CertificationMapper,
    EducationMapper,
    ExperienceMapper,
    ProjectsMapper,
)


class BuilderService:
    _CATEGORY_REGEX = r"(## )([\S ]+)"
    _RESUME_MAPPERS = {
        "Experience": ExperienceMapper,
        "Education": EducationMapper,
        "Certification": CertificationMapper,
        "Projects": ProjectsMapper,
    }

    def __init__(
        self,
        file_path: str,
        person_name: str = "Lukasz Zmudzinski",
        person_title: str = "Python Developer",
        person_contact: list[str] | None = None,
    ) -> None:
        self._file_path = file_path
        self._person = {
            "name": person_name,
            "title": person_title,
            "contact": person_contact or ["lukasz@zmudzinski.me", "github.com/lukzmu"],
        }

    def build(self) -> None:
        file_output = self._process_file(file_path=self._file_path)
        html_output = self._create_html(template_data=file_output)
        self._create_pdf(html=html_output)

    def _process_file(self, file_path: str) -> dict[str, Any]:
        output: dict[str, Any] = {"personal_info": self._person}

        with open(file_path) as file:
            category_data: dict[str, list[str]] = {}
            last_category: str | None = None
            for line in file:
                clean_line = line.strip("\n")

                if form := re.match(self._CATEGORY_REGEX, clean_line):
                    last_category = form.group(2)
                    category_data[last_category] = []
                    continue

                if last_category and clean_line:
                    category_data[last_category].append(clean_line)

        for category, items in category_data.items():
            if category in self._RESUME_MAPPERS:
                mapped_category = self._RESUME_MAPPERS[category].map(data=items)
                output[category] = mapped_category

        return output

    @staticmethod
    def _create_html(template_data: dict[str, Any]) -> str:
        environment = Environment(loader=FileSystemLoader("resume/templates/"))
        template = environment.get_template("resume.html")
        return template.render(template_data)

    @staticmethod
    def _create_pdf(html: str) -> None:
        pdfkit.from_string(input=html, output_path="resume.pdf")
