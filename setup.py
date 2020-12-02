import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FPL_team_selector",
    version="0.0.1",
    author="Abdulrahman Elgendy",
    author_email="Abdul.Elgendy@outlook.com",
    description="This package selects the best 15 players to choose when playing a wildcard on Fantasy premier league on any given week",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdul-gendy/Fantasy_Premier_League_Team_Selector",
    download_url=,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests","pandas","PuLP",],
    python_requires='>=3.6',
)