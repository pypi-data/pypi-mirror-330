import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='qtility',
    version='0.1.1',
    author='Mike Malinowski',
    author_email='mike.external@outlook.com',
    description='Support functions for working with PySide2/PySide6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikemalinowski/qtility',
    python_requires='>3.5.2',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "scribble",
    ],
    keywords="pyside pyside2 pyside6 pyqt4 pyqt5 malinowski",
)
