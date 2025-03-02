from setuptools import setup, find_packages

setup(
    name="scalar-docs",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    extras_require={
        "django_example": ["django"],
        "fastapi_example": ["fastapi"],
        "flask_example": ["flask"],
    },
    description="A Python port of the Scalar API documentation library.",
    author="Oscar Rivas",
    author_email="80918302+OscarRG@noreply.users.github.com",
    url="https://github.com/OscarRG/scalar-py",
)
