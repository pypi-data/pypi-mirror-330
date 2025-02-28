from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sentiframe",
    version="0.1.0",
    author="Ayush Rawat",
    author_email="ayushrawat220804@gmail.com",
    description="A flexible framework for scraping and analyzing YouTube comments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayushrawat220804/sentiframe",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-api-python-client>=2.108.0",
        "python-dotenv>=1.0.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "web": ["streamlit>=1.29.0"],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sentiframe-web=sentiframe.web.app:main [web]",
        ],
    },
    keywords=["youtube", "comments", "analysis", "sentiment", "api"],
    project_urls={
        "Bug Reports": "https://github.com/ayushrawat220804/sentiframe/issues",
        "Source": "https://github.com/ayushrawat220804/sentiframe",
        "Documentation": "https://github.com/ayushrawat220804/sentiframe#readme",
    },
) 