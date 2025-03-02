from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dataflowtool",
    version="1.0.0",  # First stable release
    author="Anirudh",
    author_email="isanirudhonline@gmail.com",
    description="A modern data lineage visualization tool with column-level dependency tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dataflowtool",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "dataflowtool": ["frontend/dist/*", "frontend/dist/assets/*"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "dbt-core>=1.4.0",
        "networkx>=2.6.0",
        "pydantic>=1.8.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dataflowtool=dataflowtool.server:run_server",
        ],
    },
    keywords="data lineage, dbt, visualization, data dependencies, column lineage",
) 