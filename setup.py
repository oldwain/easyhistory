from setuptools import setup

import easyhistory

long_desc = """
easyhistory
"""

setup(
        name='easyhistory',
        description='easyhistory',
        long_description=long_desc,
        author='shidenggui',
        author_email='longlyshidenggui@gmail.com',
        license='BSD',
        url='https://github.com/shidenggui/easyqhistory',
        keywords='China stock trade',
        install_requires=['pandas', 'TA-LIB', 'requests', 'pyquery'],
        classifiers=['Development Status :: 4 - Beta',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: BSD License'],
        packages=['easyhistory'],
        package_data={'': ['*.conf']}
)
