from setuptools import setup, find_packages

setup(
    name="banyarag",
    version="0.1.20",
    description="Banya RAG file uploader and training library",
    author="smkim",
    author_email="ksm@daiblab.com",
    url="https://github.com/DaiosFoundations/banyarag",  # GitHub 또는 프로젝트 URL
    packages=find_packages(),
    install_requires=[
        "requests",  # 외부 종속성
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)


# python setup.py sdist bdist_wheel && python -m twine upload dist/*
# source .venv/bin/activate
# pip install banyarag --upgrade