import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rayson",  # Your package name
    version="0.0.3",
    author="Rayid Ahmed",
    author_email="rayidahmed@gmail.com",
    description="Generate scripts for JSON instantly for faster development and testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ray837/JSONQL",  # Update with your repository URL
    packages=setuptools.find_packages(),  # Automatically finds the package(s) (rayson)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
