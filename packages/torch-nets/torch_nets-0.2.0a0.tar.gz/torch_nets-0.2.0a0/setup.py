# -- import packages: ---------------------------------------------------------
import setuptools

# -- run setup: ---------------------------------------------------------------
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("torch_nets/__version__.py") as v:
    exec(v.read())

setuptools.setup(
    name="torch-nets",
    version=__version__,
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard.ai@gmail.com",
    url=None,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="API to compose PyTorch neural networks on the fly.",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
