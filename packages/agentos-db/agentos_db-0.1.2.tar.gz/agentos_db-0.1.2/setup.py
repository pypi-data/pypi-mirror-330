from setuptools import setup, find_packages

setup(
    name="agentos-db",
    packages=find_packages(
        include=["agentos_db", "agentos_db.*"]
    ),  # This will include all subpackages
    version="0.1.2",
    author="AgentOS",
    description="The shared database for AgentOS",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.0",
        # other dependencies
    ],
)
