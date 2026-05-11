"""
setup.py
--------
Makes the project installable as a local Python package.

After running `pip install -e .` from the project root, you can import
any module from `src/dsproject/` using:

    from dsproject.logger import get_logger
    from dsproject.components.data_ingestion import DataIngestion

The `-e` (editable) flag means changes to source files are reflected
immediately without reinstalling.
"""

from setuptools import setup, find_packages


def get_requirements(filepath: str) -> list[str]:
    """
    Read requirements.txt and return a list of package names.
    Filters out comment lines and the '-e .' editable-install marker.
    """
    requirements = []
    with open(filepath, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            # Skip blank lines, comments, and editable install markers
            if line and not line.startswith("#") and line != "-e .":
                requirements.append(line)
    return requirements


setup(
    name="dsproject",
    version="0.1.0",
    author="Pranav Dhadwal",
    author_email="dhadwal.pranav01@gmail.com",
    description="Customer Churn Prediction — Production-grade MLOps pipeline",
    # long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    # long_description_content_type="text/markdown",
    url="https://github.com/Pranav-Dhadwal/dsproject",
    # find_packages(where="src") discovers all packages inside the src/ directory
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=get_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Customer Churn Prediction :: ML",
    ]
)
