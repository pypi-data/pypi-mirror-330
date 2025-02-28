from setuptools import setup, find_packages

setup(
    name='cos-viewer',
    version='0.1.2',
    description='A COS viewer application',

    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'textual>=0.34.0',
        'cos-python-sdk-v5>=1.9.34',
        'python-dotenv>=0.19.0',
        'pathlib>=1.0.1',
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'src': ['cos_viewer/css/*.css', 'requirements.txt'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cos-viewer=src.main:start',
        ],
    },
)
