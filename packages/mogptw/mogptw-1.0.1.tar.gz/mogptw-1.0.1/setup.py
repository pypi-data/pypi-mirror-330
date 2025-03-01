from setuptools import setup

setup(
    name='mogptw',
    version='1.0.1',
    description='Mixture of Gaussian Processes Model for Sparse Longitudinal Data',
    url='https://github.com/fraenkel-lab/mogp',
    python_requires='>=3.8',
    packages=['mogp'],
    # package_data={'mogp': ['data/reference_model.pkl']},

    install_requires=[
       'numpy>=1.25, <2',
       'GPy==1.13.2',
       'scikit-learn',
       'matplotlib',
       'pytest'],

# python 3.7.3 reqs:
#    install_requires=[
#        'GPy==1.9.9',
#        'scipy>=1.3.0',
#        'numpy>=1.16.4,<1.20',
#        'scikit-learn==0.21.1',
#        'sklearn>=0.0',
#        'matplotlib>=3.1.1'],

    author='Divya Ramamoorthy',
    author_email='divyar@mit.edu',
    license='MIT'
)
