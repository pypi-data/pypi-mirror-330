from setuptools import setup, find_packages

setup(
    name="docx2daisy",
    version="0.1.0",
    description="A Python library for converting .docx files to DAISY 3 digital books",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/DOCX2DAISY",
    packages=find_packages(),  # Automatically find packages under docx2daisy/
    install_requires=[
        "python-docx>=0.8.11",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
