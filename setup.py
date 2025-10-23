from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")
else:
    long_description = ("BOM to LCSC Part Matcher - Fuzzy search tool for "
                        "electronic components")

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    requirements = [
        line.strip()
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
else:
    # Fallback to minimal requirements if file doesn't exist
    requirements = [
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "xlwings>=0.30.0",
        "pandas>=2.1.0",
        "rapidfuzz>=3.5.0",
        "pillow>=10.1.0",
        "pyyaml>=6.0.1",
        "python-dateutil>=2.8.2",
        "tqdm>=4.66.0",
        "pydantic>=2.5.0",
        "diskcache>=5.6.3",
    ]

setup(
    name="lhatolcsc",
    version="0.2.5",
    author="Your Name",
    author_email="your.email@example.com",
    description="BOM to LCSC Part Matcher - Fuzzy search tool for electronic components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/LHAtoLCSC",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/LHAtoLCSC/issues",
        "Documentation": "https://github.com/yourusername/LHAtoLCSC/docs",
        "Source Code": "https://github.com/yourusername/LHAtoLCSC",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: X11 Applications",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lhatolcsc=lhatolcsc.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lhatolcsc": [
            "resources/icons/*.png",
            "resources/config/*.json",
        ],
    },
    zip_safe=False,
)
