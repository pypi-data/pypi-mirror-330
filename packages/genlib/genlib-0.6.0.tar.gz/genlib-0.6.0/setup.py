from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name='genlib',
    version='0.6.0',
    description='This is the basic library for xkit.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chanmin.park',
    author_email='devcamp@gmail.com',
    url='https://github.com/planxstudio/xkit',
    install_requires=['ifaddr'],
    packages=find_packages(exclude=[]),    
    keywords=['xkit'],
    python_requires='>=3.8',
    package_data={}, 
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
