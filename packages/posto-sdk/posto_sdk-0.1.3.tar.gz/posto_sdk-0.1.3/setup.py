from setuptools import setup, find_packages

setup(
    name="posto-sdk",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.0",
        "python-dateutil>=2.8.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=22.0.0",
            "flake8>=3.9.0",
        ],
    },
    author="Eli",
    author_email="eli@posto.io",
    description="A powerful Python SDK for managing and automating social media posts across multiple platforms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/posto-io/posto-sdk",
    project_urls={
        "Documentation": "https://github.com/posto-io/posto-sdk#readme",
        "Bug Reports": "https://github.com/posto-io/posto-sdk/issues",
        "Source Code": "https://github.com/posto-io/posto-sdk",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Communications",
    ],
    python_requires=">=3.7",
    keywords="social media, automation, posting, scheduling, facebook, twitter, instagram, linkedin",
)

