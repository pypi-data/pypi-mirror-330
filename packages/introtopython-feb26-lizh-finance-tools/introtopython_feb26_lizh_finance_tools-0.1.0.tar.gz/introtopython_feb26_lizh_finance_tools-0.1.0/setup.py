from setuptools import setup, find_packages


setup(
    name='introtopython-feb26-lizh-finance-tools',
    version='0.1.0',
    packages=find_packages("."),
    install_requires=[
        'numpy',
        'pandas'
    ],
    author='Liz Howard',
    description="""
    A collection of tools for financial analysis
    """,
    license='MIT',
)