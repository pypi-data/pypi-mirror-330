from setuptools import setup, find_packages  

setup(  
    name='elfi-python-sdk',  
    version='1.0.6',  
    author='0xELFi',  
    author_email='0xELFi@elfi.com',  
    description='ELFi Protocol python sdk',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/0xCedar/elfi_python_sdk',  
    packages=find_packages(),  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.10',  
    install_requires=[  
        'Requests==2.32.3',
        'web3==7.4.0'
    ],
    include_package_data=True,    
    package_data={  
        '': ['abis/*.json'],
        'abis': ['*.json'],  
    }  
)  