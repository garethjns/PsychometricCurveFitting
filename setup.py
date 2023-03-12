import setuptools

from fit_psyche import __version__

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FitPsyche",
    version=__version__,
    author="Gareth Jones",
    author_email="garethgithub@gmail.com",
    description="Psychometric curve fitting package for Python and MATLAB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/garethjns/PsychometricCurveFitting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"],
    python_requires='>=3.6',
    install_requires=['scipy', 'numpy', 'scikit-learn', 'matplotlib'])
