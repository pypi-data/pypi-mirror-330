from setuptools import setup

setup(
    name="dino-run-run-run",
    version="1.0.2",
    py_modules=["dinosaur"],
    entry_points={
        "console_scripts": [
            "dino-run-run-run = dinosaur:game",
        ],
    },
)
