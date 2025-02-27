from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

dependencies = ['httpx']

setup(
    name='sigmasms',
    version='1.2.1',
    description='Tool for easy working with SigmaSMS API',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Anton Shchetikhin',
    author_email='animal2k@gmail.com',
    py_modules=['sigmasms'],
    install_requires=['httpx'],
    url='https://github.com/mrslow/sigmasms',
    keywords='api sigmasms client',
    packages=find_packages(),
    python_requires='>=3.10'
)
