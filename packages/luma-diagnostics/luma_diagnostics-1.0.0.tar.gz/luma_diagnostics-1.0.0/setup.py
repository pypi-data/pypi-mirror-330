from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        "requests>=2.25.1",
        "python-dotenv>=0.19.0",
        "pillow>=8.3.1",  # For image validation
        "dnspython>=2.1.0",  # For DNS lookups
        "certifi>=2021.5.30",  # For SSL certificate validation
        "questionary>=1.10.0",  # For interactive prompts
        "rich>=10.6.0",  # For console output formatting
        "psutil>=5.8.0",  # For system information collection
    ]

test_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pillow>=8.3.1",  # For image validation
    "numpy>=1.21.0",  # For test image generation
]

setup(
    name="luma-diagnostics",
    version="1.0.0",
    author="Casey Fenton",
    author_email="casey@caseyfenton.com",
    description="An unofficial diagnostic tool for troubleshooting LUMA Dream Machine API issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caseyfenton/luma-diagnostics",
    project_urls={
        "Bug Tracker": "https://github.com/caseyfenton/luma-diagnostics/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "test": test_requirements,
    },
    entry_points={
        "console_scripts": [
            "luma-diagnostics=luma_diagnostics.cli:main",
        ],
    },
    package_data={
        "luma_diagnostics": [
            "templates/*",
            "cases/templates/*"
        ],
    },
)
