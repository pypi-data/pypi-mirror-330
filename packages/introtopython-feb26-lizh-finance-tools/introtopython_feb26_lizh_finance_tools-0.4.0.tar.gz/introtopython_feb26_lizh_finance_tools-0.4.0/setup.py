from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        print("Running custom installation steps...")
        print("stealing all your data")
        super().run()
        print("all your data are belong to us")
        
setup(
    name='introtopython-feb26-lizh-finance-tools',
    version='0.4.0',
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
    cmdclass={
        'install': CustomInstall
    }
)