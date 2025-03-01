from setuptools import setup, find_packages

setup(
    name="code2uml",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'code2uml=code2uml.code2uml:main',
        ],
    },
    install_requires=[
        'antlr4-python3-runtime'
    ],
    description='Generate UML diagrams from source code',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    author='min',
    author_email='testmin@outlook.com',
    url='https://gitee.com/jakHall/code2uml.git',
)
