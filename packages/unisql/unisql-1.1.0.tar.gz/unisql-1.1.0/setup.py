from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="unisql",
    version="1.1.0",
    author="Joumaico Maulas",
    description="SQL Database Wrapper",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/joumaico/unisql",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    packages=[
        "unisql",
    ],
    package_dir={
        "unisql": "src/unisql",
    },
    python_requires=">=3.8",
    install_requires=[
        "aiosqlite",
        "asyncpg",
        "psycopg2-binary",
        "pymysql",
    ],
)
