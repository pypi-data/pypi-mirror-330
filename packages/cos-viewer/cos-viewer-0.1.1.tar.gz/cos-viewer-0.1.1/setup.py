from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='cos-viewer',
    version='0.1.1',
    description='A COS viewer application',
    
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'src': ['cos_viewer/css/*.css'],
        'requirements.txt': ['requirements.txt'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cos-viewer=src.main:start',
        ],
    },
)
