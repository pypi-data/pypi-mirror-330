from setuptools import setup, find_packages

setup(
    name="subito-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open('requirements.txt')
        if line.strip() and not line.startswith('#')
    ],
    entry_points={
        "console_scripts": [
            "subito=subito_client.cli:main",
        ],
    },
    author="hernehunter",
    author_email="h3rn3hunt3r@gmail.com",
    description="A subtitle translator that utilizes LLMs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hernehunter/subito-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    package_data={
        'subito_client.configs': ['*.yml'],
    },
    include_package_data=True,
)
