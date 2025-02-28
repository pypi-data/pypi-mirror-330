from setuptools import setup

setup(
    name='plover-dani-machine',  # MUST start with "plover-"
    version='0.1.0',
    description='My custom Plover machine using the English alphabet',
    author='Your Name',
    packages=['plover_dani_machine'],
    entry_points={
        'plover.machine': [
            'dani_key_en = plover_dani_machine.dani_key_en:dani_key_En',
        ],
    },
    install_requires=['plover>=4.0.0'],
    python_requires='>=3.7',
    # Classifiers are optional but can help
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
