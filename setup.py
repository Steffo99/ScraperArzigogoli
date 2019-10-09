import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="arzibot",
    version="0.1",
    author="Federico Fantini",
    author_email="federico.fantini.developer@gmail.com",
    description="A web scraper for the Arzigogoli of Sistemi Operativi at Unimore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/federicofantinidev/ScraperArzigogoli",
    packages=setuptools.find_packages(),
    install_requires=["requests", "bs4"],
    python_requires=">=3.7",
    classifiers=[]
)
