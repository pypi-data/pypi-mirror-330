from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()
    
setup(
    name="Fragpy",
    version="0.0.1",
    description="An async A Python library for interacting with fragment.com API, supporting session-based authentication and real-time updates.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Muamel Ameer",
    author_email="amowallet@gmail.com",
    url="https://github.com/aamole/fragpy",
    license="MIT",
    python_requires=">=3.8",
    project_urls={
        "Source": "https://github.com/aamole/fragpy",
        "Tracker": "https://github.com/aamole/fragpy/issues",
    },
    packages=[""],
    keywords=[
        "sync",
        "asyncio",
        "aiohttp",
        "sqlite3",
        "kvsqlite",
        "fragment-apis",
        "fragment",
        "client"
    ],
)