from setuptools import setup, find_packages

setup(
    name='ml_ops_mironov',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    author='Mironov Ilya',
    author_email='ilyamironov2102@gail.com',
    description='ML OPS'
,
    long_description_content_type='text/markdown',
    url='https://gitlab.v-efimov.tech/mlops_spring_2025/mlops_project_mironov.nedab#',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
