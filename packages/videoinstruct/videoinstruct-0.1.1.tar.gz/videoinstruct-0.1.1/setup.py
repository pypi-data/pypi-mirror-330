from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="videoinstruct",
    version="0.1.1",
    author="Pouria Rouzrokh",
    author_email="po.rouzrokh@gmail.com",
    description="A tool that automatically generates step-by-step documentation from instructional videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PouriaRouzrokh/VideoInstruct",
    packages=find_packages(include=["videoinstruct", "videoinstruct.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "videoinstruct": ["prompts/*.md", "prompts/*.txt", "prompts/*.json"],
    },
    entry_points={
        "console_scripts": [
            "videoinstruct=videoinstruct.cli:main",
        ],
    },
) 