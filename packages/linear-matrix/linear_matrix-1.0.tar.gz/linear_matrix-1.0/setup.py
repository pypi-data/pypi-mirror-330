from setuptools import setup, find_packages

setup(
    name="linear_matrix",
    version="1.0",
    author="Sourceduty",
    author_email="sourceduty@gmail.com",
    description="A Python library for linear algebra matrix operations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://sourceduty.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
