from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="email-processor-cli",
    version="2025.10.28.192459",
    author="Anderson Taguada",
    author_email="ferchoafta@gmail.com",
    description="CLI tool for email processing with domain migration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anders2D/email-domain-migration-processor",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=3.0.0",
        "requests>=2.31.0",
        "openpyxl>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "email-processor=src.features.email_processing.adapters.input.cli_entrypoint:main",
        ],
    },
    include_package_data=True,
    keywords="email processing cli domain migration automation",
    project_urls={
        "Bug Reports": "https://github.com/anders2D/email-domain-migration-processor/issues",
        "Source": "https://github.com/anders2D/email-domain-migration-processor",
        "Documentation": "https://github.com/anders2D/email-domain-migration-processor/blob/main/README.md",
    },
)
