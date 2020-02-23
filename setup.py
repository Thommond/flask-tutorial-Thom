import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="flask-tutorial"
    version="0.0.1",
    author="Thom Mondeaux",
    author_email="Thommond@protonmail.com",
    url="https://github.com/Thommond/flask-tutorial-Thom",
    description="A basic tutorial for the ropes of Flask.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[],
    extras_require=[],
    tests_require=['pytest'],
    python_requires='>=3.6',
)
