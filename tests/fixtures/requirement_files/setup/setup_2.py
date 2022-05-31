from setuptools import setup

setup(
    name="autorate",
    version="0.1.0",
    author="Eshan King,  Davis Weaver",
    author_email="",
    packages=["autorate", "autorate.test", "autorate.test.data"],
    install_requires=[
        "pandas",
        "pytest",
        "scipy",
        "matplotlib",
        "numpy",
        "importlib_resources",
    ],
    include_package_data=True,
    package_data={"": ["data/*.csv"]},
)
