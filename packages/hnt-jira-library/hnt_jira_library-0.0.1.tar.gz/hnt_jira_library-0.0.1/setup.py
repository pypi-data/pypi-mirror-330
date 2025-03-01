from setuptools import setup, find_packages

setup(
    name='hnt_jira_library',
    version='0.0.1',
    license='MIT License',
    author='Pepe',
    maintainer='Pepe',
    keywords='jira',
    description=u'Lib to download from Jira attachments',
    packages=find_packages(),
    package_data={'hnt_jira': ['attachment/*']},
    include_package_data=True,
    install_requires=[
        'requests'
    ],
)