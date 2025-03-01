from setuptools import setup, find_packages

setup(
    name="datetime_utils-sribandi",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytz"
    ],
    author="Srinidhi Bandi",  # Replace with your actual name
    description="A Python library for date and time utilities",
    url="https://github.com/srinidhi-bandi/Datetime-Utilities",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
 
