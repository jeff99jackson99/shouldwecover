from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="insurance-claim-analyzer",
    version="1.0.0",
    author="Insurance Claims Team",
    author_email="team@insurance-analyzer.com",
    description="AI-powered insurance claim coverage analyzer using Streamlit and OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/insurance-claim-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Insurance",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.6",
            "black>=23.11.0",
            "mypy>=1.7.1",
            "safety>=2.3.0",
            "bandit>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "insurance-analyzer=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
)
