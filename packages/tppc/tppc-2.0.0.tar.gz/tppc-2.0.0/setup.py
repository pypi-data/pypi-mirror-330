from setuptools import setup, find_packages

setup(
    name='tppc',
    version='2.0.0',
    author='Your Name',
    author_email='your-email@example.com',
    description='Optimized T++ Compiler & Execution Engine',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourrepo/tppc',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tppc=tppc.main:run'
        ]
    },
    install_requires=[
        'requests', 'cryptography', 'numpy', 'pycryptodome'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
)
