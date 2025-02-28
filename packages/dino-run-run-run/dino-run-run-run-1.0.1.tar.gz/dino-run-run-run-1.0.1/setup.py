from setuptools import setup

setup(
    name="dino-run-run-run",
    version="1.0.1",
    py_modules=["dinosaur"],
    entry_points={
        "console_scripts": [
            "dinogame = dinosaur:game",
        ],
    },
)
