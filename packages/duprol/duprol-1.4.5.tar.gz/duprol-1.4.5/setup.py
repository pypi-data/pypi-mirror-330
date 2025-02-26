from setuptools import setup

setup(
    name="duprol",
    version="1.4.5",
    install_requires=["dill"],  # Add dependencies if needed
    author="Darren Chase Papa",
    author_email="darrenchasepapa@gmail.com",
    description="A dumb programming language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
