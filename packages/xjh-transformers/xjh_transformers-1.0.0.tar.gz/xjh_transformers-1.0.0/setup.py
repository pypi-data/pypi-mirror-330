from setuptools import setup, find_packages
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xjh_transformers",
    version="1.0.0",
    author="xjh",
    author_email="xujiahao056@gmailc.om",
    packages=find_packages(),
    python_requires='>=3.6',
)