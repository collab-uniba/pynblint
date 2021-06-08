import setuptools

setuptools.setup(
    name="pynblint",
    version="0.1.0",
    author="Luigi Quaranta",
    author_email="luigi.quaranta@uniba.it",
    description="A linting library for Jupyter notebooks.",
    packages=["pynblint"],

    include_package_data=True,
    python_requires=">=3.7.10",
    install_requires=[
        "ipython",
        "nbformat",
        "nbconvert",
        "GitPython"
    ],
    entry_points={
        "console_scripts": [
            "pynblint=pynblint.__main__:main",
        ]
    },
)
