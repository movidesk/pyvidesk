from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyvidesk",
    version="0.0.1",
    author="Murilo Scarpa Sitonio",
    author_email="muriloscarpa@gmail.com",
    description="Movidesk API client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/movidesk/pyvidesk",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.8.2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests>=2.0", "python-dateutil"],
    extras_require={"dev": ["black", "bandit", "pylint", "python-decouple"]},
    python_requires=">=3.7",
)
