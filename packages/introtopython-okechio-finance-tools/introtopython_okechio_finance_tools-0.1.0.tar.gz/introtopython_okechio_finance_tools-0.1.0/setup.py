from setuptools import setup, find_packages

#command to run to install package: "pip install -e . "

setup(
    name='introtopython-okechio-finance-tools',
    version='0.1.0',
    packages=find_packages("."),
    install_requires=[
        'numpy',
        'pandas'
    ],
    author='Okechi Osuagwu',
    description="""
    A collection of tools for finacial analysis
    """,
    license='MIT'
)