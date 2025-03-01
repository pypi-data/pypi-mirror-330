from setuptools import setup, find_packages

setup(
    name="aiba-lang",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygments",
        "jedi",
        "diffusers",
        "transformers",
        "torch",
        "requests",
        "boto3",
        "psutil",
        "tensorflow",
        "opencv-python",
        "numba",
        "llvmlite",
        "tk"
    ],
    entry_points={
        "console_scripts": [
            "aiba=aiba_compiler:main",
            "aiba-ide=aiba_ide:main",
            "aiba-pkg=aiba_pkg_manager:main"
        ]
    },
    author="Seu Nome",
    description="AIBA - Linguagem de Programação para Inteligência Artificial",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/aiba-lang",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
