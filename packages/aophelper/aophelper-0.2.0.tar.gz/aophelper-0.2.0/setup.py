from setuptools import setup, find_packages

setup(
    name="aophelper",
    version="0.2.0",  # 버전
    author="mathbook3948",  # 작성자
    author_email="yuno.jung.07@gmail.com",  # 이메일
    description="AOP (Aspect-Oriented Programming) helper for Python",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mathbook3948/AOPHelper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)