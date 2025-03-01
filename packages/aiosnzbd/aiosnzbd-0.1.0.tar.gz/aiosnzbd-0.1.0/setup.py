from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aiosnzbd",
    version="0.1.0",  # Initial release version
    author="Andrews Jack",
    author_email="",
    description="Complete Asynchronous API wrapper for the usenet downloading tool SABnzbd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',  # Specify the Python version compatibility
    install_requires=[
        "httpx",  # Add your package dependencies here
        "urllib3"
    ],
    license="MIT",  # Replace with your chosen license
    keywords="sabnzbd async client api wrapper",  # Add relevant keywords
)
