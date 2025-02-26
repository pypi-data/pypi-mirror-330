from setuptools import setup, find_packages

setup(
    name='rsshub_twitter_reader',
    version='0.0.4',
    description='RSSHub Twitter Reader: Captura de tweets via RSS com filtragem por palavras-chave',
    long_description='RSSHub Twitter Reader: Captura de tweets via RSS com filtragem por palavras-chave',
    long_description_content_type='text/markdown',
    author='Flavio Lopes',
    author_email='flavio.lopes@ideiasfactory.tech',
    url='https://github.com/dadosnapratica/rsshub_twitter_reader',
    license='MIT',
    license_files=['LICENSE'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'lxml'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)