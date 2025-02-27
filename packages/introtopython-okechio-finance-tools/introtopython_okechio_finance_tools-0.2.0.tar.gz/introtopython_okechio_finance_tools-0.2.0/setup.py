from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        print("Running custom installation steps...")
        print("stealing all your data")
        super().run()
        print("all your data belong to us")

#command to run to install package: "pip install -e . "

setup(
    name='introtopython-okechio-finance-tools',
    version='0.2.0',
    packages=find_packages("."),
    install_requires=[
        'numpy',
        'pandas'
    ],
    author='Okechi Osuagwu',
    description="""
    A collection of tools for financial analysis
    """,
    license='MIT',
    cmdclass={
        'install': CustomInstall
    }
)