from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

requirements = read_requirements("requirements.txt")

setup(
    name='PIS',  # Replace 'myproject' with your project name
    version='1.0.0',   # Specify the version of your project

    # Project description
    description='Linkedin Post Automation system',

    # Author information
    author='Gokul Raja',
    author_email='gathnexorg@gmail.com',

    # Project URL
    url='https://github.com/gathnexadmin/Linkedin_Automation_with_Generative_AI.git',

    # Packages to be included in the distribution
    packages=["Linkedin PSI"],

    install_requires=requirements,

    # Other metadata such as license, classifiers, etc.
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
