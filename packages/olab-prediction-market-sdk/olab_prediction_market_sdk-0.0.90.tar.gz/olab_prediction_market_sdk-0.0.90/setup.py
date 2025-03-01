from setuptools import setup, find_packages

NAME = "olab_prediction_market_sdk"
VERSION = "0.0.90"

setup(
    name=NAME,
    version=VERSION,
    description="OLAB Prediction Market Open API",
    author="nik.opinionlabs",
    author_email="nik@opinionlabs.xyz",
    url="",
    keywords=["PredictionMarket"],
    install_requires=[
        "urllib3 >= 2.3.0",
        "six >= 1.17.0",
        "certifi >= 2024.12.14",
        "python-dateutil >= 2.9.0.post0",
        "hexbytes >= 1.2.1",
        "web3 >= 7.6.1",
        "eth_account >= 0.13.0",
        "poly_eip712_structs >= 0.0.1",
        "olab_open_api >= 0.0.6",
        'pytest',
    ],
    packages=find_packages(),
    include_package_data=True,
)
