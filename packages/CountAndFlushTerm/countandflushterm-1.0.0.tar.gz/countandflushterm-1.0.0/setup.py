from setuptools import setup, find_packages

setup(
    name="CountAndFlushTerm",
    version="1.0.0",
    description="The script counts how many times it has been executed in the terminal and clears the terminal when it reaches the given limit.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Raxmatulloxswe",
    author_email="mr.rahmatilloh@gmail.com",
    url="https://github.com/raxmatulloxswe/PlusNWipe",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # Paket uchun talab qilinadigan kutubxonalarni ko'rsating
    # install_requires=[
    #     "aiohttp>=3.8.0",
    # ],
)

