from setuptools import setup, find_packages
from ktdparser.config import settings


def readme():
    with open(settings.README, "r") as f:
        return f.read()


setup(
  name=settings.PROJECT_NAME,
  version=settings.PROJECT_VERSION,
  description=settings.DESCRIPTION,
  long_description=readme(),
  long_description_content_type="text/markdown",
  packages=find_packages(),
  install_requires=["tabula-py", "PyPDF2", "tqdm", "psycopg2-binary", "openpyxl", "pandas"],
  python_requires=">=3.10"
)
