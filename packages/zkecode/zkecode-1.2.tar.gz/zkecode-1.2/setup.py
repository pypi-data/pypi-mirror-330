import setuptools
from pathlib import Path

setuptools.setup(
    name="zkecode",
    version=1.2,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"])
    #查找软件包，排除[test,data]这两个目录
)
