from setuptools import setup, find_packages

setup(
    name="myDataStructure",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    author="Imanol",
    author_email="imanolsupo669@example.com",
    description="A custom data structure package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myDataStructure",  # Change if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

