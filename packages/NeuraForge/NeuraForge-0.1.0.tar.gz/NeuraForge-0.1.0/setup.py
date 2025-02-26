from setuptools import setup, find_packages

setup(
    name='NeuraForge',  # Replace with your library name
    version='0.1.0',  # Start with an initial version
    description='A basic AI library built off of google gemini api',
    long_description=open(r'C:\Users\priti\Downloads\NeuraForge\README.md').read(),  # Make sure you have a README.md file
    long_description_content_type='text/markdown',
    author='Aaroh Charne',  # Replace with your name
    author_email='aaroh.charne@gmail.com',  # Replace with your email
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'google.generativeai',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.9',  # Specify the Python version required
)