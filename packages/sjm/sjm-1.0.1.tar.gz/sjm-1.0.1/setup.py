from setuptools import setup, find_packages

setup(
    name="sjm", 
    version="1.0.1",
    packages=find_packages(),
    install_requires=["requests"],  # Add any necessary dependencies
    author="sjm",
    author_email="snappyjobs.ai@gmail.com",
    description="SJM: AI-powered freelancing and interview automation",
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Uses README for PyPI page
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/sjm/",  # PyPI project link
    project_urls={
        "Documentation": "https://your-api-docs-url.com",
        "Github": "https://github.com/snappyjobai/sjmai",
        "Issue Tracker": "https://github.com/snappyjobai/sjm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
)

