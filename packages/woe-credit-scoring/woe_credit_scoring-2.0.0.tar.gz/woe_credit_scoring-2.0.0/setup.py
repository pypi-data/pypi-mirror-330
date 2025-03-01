from setuptools import setup, find_packages

setup(
    name="woe-credit-scoring",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["numpy>=2.2.3",
                      "pandas>=2.2.3",
                      "scikit-learn>=1.6.1",
                      "matplotlib>=3.10.1",
                      "seaborn>=0.13.2",
                      "scipy>=1.15.2"
],
    author="José G. Fuentes,PhD",
    author_email="jose.gustavo.fuentes@comunidad.unam.mx",
    description="Tools for creating credit scoring models",
    long_description=open("README.md").read(),
    url = "https://github.com/JGFuentesC/woe_credit_scoring",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.13',
)
