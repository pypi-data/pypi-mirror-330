from setuptools import setup, find_packages

setup(
    name="szn_url",
    version="1.0.2",
    packages=find_packages(),
    description="A demo package that downloads OS-specific and test manuals on initialization.",
    author="Pen Test",
    author_email="test.skvara2@seznam.cz",
    url="https://example.com/szn_url",
    install_requires=[
        # Add any package dependencies here.
    ],
    entry_points={
        "console_scripts": [
            "szn_url=szn_url.__init__:main",
        ],
    },
)
