from setuptools import setup, find_packages

setup(
    name="demo-project-suthish",  # Replace with your package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SuthishSurendran/demo-project-suthish",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
