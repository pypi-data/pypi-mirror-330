from setuptools import setup, find_packages

setup(
    name="hblang",
    version="1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hblang = hblang.interpreter:main",
        ],
    },
    install_requires=[
        "requests",
    ],
    description="Интерпретатор для языка .hb",
    author="hosarov",
    author_email="CndCrime@proton.me",
    url="https://github.com/Hosarov",
)