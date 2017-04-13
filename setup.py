from setuptools import setup
from aiounfurl import VERSION


readme_file_path = 'README.md'
setup(
    name="aiounfurl",
    version=".".join(map(str, VERSION)),
    author="Igor Tokarev",
    author_email="TigorC@gmail.com",
    description='Making site preview',
    long_description=open(readme_file_path).read(),
    license="BSD License",
    keywords="sync embed preview",
    url="https://github.com/tigorc/aiounfurl",
    include_package_data=True,
    install_requires=[
        'setuptools',
        'beautifulsoup4',
        'html5lib==1.0b8',
        'requests'],
    packages=['aiounfurl'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP"
    ],
)
