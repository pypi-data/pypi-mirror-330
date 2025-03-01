from setuptools import setup, find_packages

setup(
    name="pywmm",
    version="0.1.0",
    description="World Magnetic Model (WMM) calculations",
    author="Douglas Rojas",
    author_email="dougcr95@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pywmm": ["data/WMM.COF"],
    },
    install_requires=[
        "numpy",
    ],
)
