from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dataflowtool",
    version="0.1.1",
    author="Anirudh",
    author_email="isanirudhonline@gmail.com",
    description="A tool for visualizing data lineage and column-level dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dataflowtool",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "dataflowtool": ["frontend/dist/*", "frontend/dist/assets/*"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dataflowtool=dataflowtool.server:run_server",
        ],
    },
) 