from setuptools import setup, find_packages


setup(
    name="cldfbench_hsiuhmongmien",
    py_modules=["cldfbench_hsiuhmongmien"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "lexibank.dataset": ["hsiuhmongmien=lexibank_hsiuhmongmien:Dataset"],
        "cldfbench.commands": ["hsiuhmongmien=hsiuhmongmiencommands"],
    },
    install_requires=["pylexibank>=3.0"],
    packages=find_packages(where="."),
    extras_require={"test": ["pytest-cldf"]},
)
