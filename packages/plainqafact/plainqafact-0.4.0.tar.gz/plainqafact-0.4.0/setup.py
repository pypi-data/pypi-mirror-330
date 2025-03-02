from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='plainqafact',
    version='0.4.0',
    author='Zhiwen You',
    author_email='zhiweny2@illinois.edu',
    description='A framework for evaluating plain language summaries using question answering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zhiwenyou103/PlainQAFact',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'plainqafact': ['transformers_old_tokenizer-3.1.0-py3-none-any.whl'],
    },
    entry_points={
        'console_scripts': [
            'plainqafact=plainqafact.run:main',
        ],
    },
) 