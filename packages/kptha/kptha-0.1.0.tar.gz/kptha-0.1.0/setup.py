from setuptools import setup, find_packages

setup(
    name='kptha',
    version='0.1.0',
    description='Korean-based Python syntax translator | 한국어 파이썬 번역기',
    author='rainy58',
    author_email='yhg4908@kakao.com',
    long_description=open('README.md').read() if open('README.md', 'r').read() else '',
    long_description_content_type='text/markdown',
    project_urls={
        "Issues": "https://github.com/yhg4908/kpth/issues",
        "Repository": "https://github.com/yhg4908/kpth",
    },
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ㅋㅍ=kpth.중앙:주_실행',
        ]
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.10',
    package_data={'': ['LICENSE', 'README.md']},
    keywords='korea korean python kpy kpth 한국어 한국 파이썬',
)
