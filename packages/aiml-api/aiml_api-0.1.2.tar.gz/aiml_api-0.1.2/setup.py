from setuptools import find_packages, setup

setup(
    name="aiml_api",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "openai>=1.55.1",
        "pydantic-settings>=2.7.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
