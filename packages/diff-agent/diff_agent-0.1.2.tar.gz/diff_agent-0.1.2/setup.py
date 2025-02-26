from setuptools import setup, find_packages

setup(
    name="diff_agent",
    version="0.1.2",
    description="A tool for automatically committing and summarizing git changes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/diff_agent",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "litellm>=0.1.0",
        "weave>=0.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
