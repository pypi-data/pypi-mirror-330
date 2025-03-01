from setuptools import setup, find_packages

setup(
    name="modelscout",
    version="0.1.1",
    packages=find_packages(include=["modelscout", "modelscout.*"]),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    include_package_data=True,
    package_data={"modelscout": ["models.csv"]}, 
    entry_points={
        "console_scripts": [
            "modelscout=modelscout.cli:main",
        ],
    },
    author="Hadi Ibrahim",
    description="ModelScout: Find the best LLM for your needs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hadi-M-Ibrahim/ModelScout",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
