from setuptools import setup

setup(
    name="dino_run_run_run",
    version="1.0.3",
    py_modules=["dinosaur"],
    entry_points={
        "console_scripts": [
            "dino_run_run_run = dinosaur:main",
        ],
    },
)
