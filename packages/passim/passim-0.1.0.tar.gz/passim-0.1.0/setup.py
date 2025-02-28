from setuptools import setup, find_packages

setup(
    name='passim',
    version='0.1.0',
    author='Abdulhaleem Nasredeen',
    author_email='nabdulhaaleeem09@gmail.com',
    description="Password similarity checking using n-grams",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nasredeenabdulhaleem/passim',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=["bcrypt"],
)

