from setuptools import setup

setup(
    name="proxy-rotator-toolkit",
    version="0.0.26",
    author="Webparsers",
    author_email="panenotgeor@gmail.com",
    description="Proxy rotation is a project designed to simplify working with the proxy rotation",
    # long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
    # url="https://github.com/Web-parsers/middleman-proxy-server/tree/proxy_rotation",
    packages=[
        'proxy_rotator_toolkit',
    ],
    install_requires=[
        "apprise==1.9.1",
        "curl_cffi>=0.7.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)