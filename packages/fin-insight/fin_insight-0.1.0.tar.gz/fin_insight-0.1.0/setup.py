from setuptools import setup, find_packages

# This is now a minimal setup.py that defers most configuration to pyproject.toml
setup(
    name="fin-insight",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.38",
        "requests>=2.31.0",
        "vaderSentiment>=3.3.2",
        "pandas>=2.2.1",
    ],
    entry_points={
        'console_scripts': [
            'fin-insight=fin_insight:cli',
        ],
    },
)
