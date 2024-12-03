from setuptools import setup, find_packages

setup(
    name="sg_accident_form",
    version="1.0.0",
    description="Safety Generalist Accident Reporting System",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "inquirer==3.0.2",
        "psycopg2-binary==2.9.7",
        "openpyxl==3.1.2",
        "fpdf==1.7.2",
    ],
    entry_points={
        "console_scripts": [
            "sg_accident_form=sg_accident_form.main:main"
        ]
    },
)
