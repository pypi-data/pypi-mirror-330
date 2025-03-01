from setuptools import setup, find_packages

setup(
    name="smsmobileapi-send-email",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Quest-Concept",
    author_email="info@smsmobileapi.com",
    description="A Python module for sending emails using SMSMobileAPI directly from mailbox account",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SmsMobileApi/smsmobileapi-python-email",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
