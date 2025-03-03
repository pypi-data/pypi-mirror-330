from setuptools import setup, find_packages

setup(
    name='easyprintstr',
    version='0.1.0',
    description='A simple package to print text with a border.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='l1nyuan7',
    author_email='linyuan@gmail.com',
    url='https://github.com/l1nyuan7/easyprintstr',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',  # 指定许可证类型
    options={
        'metadata': {
            'license_file': None,  # 显式禁用 license-file
        },
    },
)