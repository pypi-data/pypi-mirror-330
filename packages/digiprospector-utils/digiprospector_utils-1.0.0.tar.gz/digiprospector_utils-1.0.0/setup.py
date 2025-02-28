from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digiprospector_utils",
    version="1.0.0",
    author="digiprospector",  # Replace with your name
    author_email="digiprospector@protonmail.com",  # Replace with your email
    description="python utils for digiprospector",  # Replace with a description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digiprospector/digiprospector_utils",  # Replace with your project URL
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose the appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # List any package dependencies here
        # "requests>=2.28.0",
        "pathlib",
        "logging",
        "colorlog"
    ],
    tests_require=[
        "pytest",
    ]
)
