from setuptools import setup, find_packages

setup(
    name="sg_accident_form",               # Name of package
    version="1.0.0",                       # Package version
    description="Safety Generalist Accident Reporting System",
    long_description=open("README.md").read(),  # Use README for a long description
    long_description_content_type="text/markdown",
    author="Cole Petty",                    # name
    author_email="colepetty57@gmail.com", # email
    url="https://github.com/pcpetty/sg_accident_form",  # URL to GitHub repo
    packages=find_packages(),              # Automatically find sub-packages
    install_requires=[
    "questionary==2.0.1",  # Use the latest version available
    "psycopg2-binary==2.9.7",
    "openpyxl==3.1.2",
    "fpdf==1.7.2",
],

    entry_points={                         # Command-line entry point
        "console_scripts": [
        "sg_accident_form=sg_accident_form.main:main"
        ]
    },
    classifiers=[                          # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",               # Minimum Python version
)
