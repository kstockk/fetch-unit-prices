from distutils.core import setup

setup(
        name='beancount-prices-custom',
        version='1.0',
        packages=['my_sources'],
        license='MIT',
        install_requires = [
                'flake8',
                'beancount'
        ]
)
