from setuptools import setup, find_packages

setup(
    name="casino1v1",
    version="0.1.0",
    author="Adarsh V H",
    author_email="adarshvh2005@gmail.com",
    description="A humorous command-line Blackjack game.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Snapout2/casino1v1.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "casino1v1=casino1v1.game:blackjack",
        ],
    },
)
