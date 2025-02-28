from setuptools import setup, find_packages

setup(
    name="track_proxy_usage_XBT",  # Unique name on PyPI
    version="0.1.0",   # First release version
    author="Bhumika Bhatti",
    author_email="bhumika.bhatti@xbyte.io",
    description="To track the proxy usage while extracting data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/my_module",  # GitHub repo (optional)
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
