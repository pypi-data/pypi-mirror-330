from setuptools import setup, find_packages

setup(
    name = "ql_sdk",      #这里是pip项目发布的名称
    version = "0.0.2",  #版本号，数值大的会优先被pip
    keywords = ("ql","青龙", "tushen"),
    description = "青龙面板API封装",
    long_description = "基于青龙面板API的封装，可以快速便捷调用面板的API",
    license = "MIT Licence",

    # url = "http://python4office.cn/upload-pip/",     #项目相关文件地址，一般是github
    author = "tushen",
    author_email = "2256485749@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]          #这个项目需要的第三方库
)