from setuptools import setup, find_packages

setup(
    name="GDReproduceConfigurationError",
    version="0.1.2",
    description="project description",
    long_description="long project description",
    author="Buenbk",   # 作者名称
    author_email="764590923@qq.com",  # 作者邮箱
    url="https://github.com/Buenbk/GDReproduceConfigurationError",  # 项目主页
    packages=find_packages(),  # 自动发现包
    install_requires=["requests"],  # 依赖项（根据需要修改）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Python 版本要求
)
