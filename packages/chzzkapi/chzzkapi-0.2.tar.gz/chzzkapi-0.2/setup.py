from setuptools import setup, find_packages

setup(
    name="chzzkapi",
    version="0.2",
    description="Chzzk API Python package",
    long_description=open('README.md', encoding='utf-8').read(),  # UTF-8로 인코딩을 명시적으로 지정
    long_description_content_type="text/markdown",
    author="Koble",
    author_email="kimkoble4@gmail.com",
    url="https://github.com/KKoble/chzzkpy",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
