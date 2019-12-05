from setuptools import setup


setup(
    name='cldfbench_hsiuhmongmien',
    py_modules=['cldfbench_hsiuhmongmien'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'hsiuhmongmien=cldfbench_hsiuhmongmien:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
