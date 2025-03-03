from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


# Основные метаданные
setup(
    name="pytopvisor",
    version="0.1.4",
    author="Dmitry Kravtsov",
    author_email="dmitry.pushpull@gmail.com",
    description="A Python client for interacting with the Topvisor API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/allcookiesaccept/PyTopvisor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.32.3",
    ],
    include_package_data=True,
)