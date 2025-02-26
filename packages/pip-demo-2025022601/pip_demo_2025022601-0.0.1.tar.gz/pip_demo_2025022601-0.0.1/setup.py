from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "pip_demo_2025022601",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ["pip", "heyWFeng"],
    description = "pip_demo desc",
    long_description = "pip_demo long desc",
    license = "MIT Licence",
    url = "https://www.baidu.com/",     #项目相关文件地址，一般是github
    author = "null",
    author_email = "1957875073@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)
