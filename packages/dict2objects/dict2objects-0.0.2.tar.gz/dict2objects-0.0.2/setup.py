from setuptools import setup, find_packages

setup(
    name="dict2objects",
    version="0.0.2",
    description="Convert Python dictionaries into objects with attribute-style access.",
    author="Janardhan Singh",
    author_email="janardhansingh1998@example.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
