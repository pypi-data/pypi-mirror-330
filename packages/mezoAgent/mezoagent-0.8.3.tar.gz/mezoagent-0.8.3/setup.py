from setuptools import setup, find_packages

setup(
    name="mezoAgent",
    version="0.8.3",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "mezo_agent": ["data/*.json"],
    },
    install_requires=[
        "python-dotenv",
        "web3",
        "langchain",
        "langchain_openai",
    ],
    author="Dreadwulf, Duck, Digi",
    description="A Python package for Mezo Agent tools with LangChain tools",
)