from setuptools import setup

setup(
    name="insights-backend",
    version="0.0.2",
    description="A backend to manage forms",
    author="Akshay Patel",
    author_email="akshay.ap95@gmail.com",
    packages=["insights-backend"],
    install_requires=["Flask", "pymongo", "python-dotenv", "bump2version"],
)
