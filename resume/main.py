import os

from builder.services import BuilderService

readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))

builder = BuilderService(file_path=readme_path)
builder.build()
