from setuptools import setup, find_packages

     
setup(
    name='MedLytics',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spacy',
        'nltk',
        'textstat',
        'textblob'
    ],
    author='Abdullah Al Fahad',
    author_email='alfahadarc@gmail.com',
    description='A text analysis package for medical text analytics using NLP libraries.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
