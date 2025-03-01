# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='deberta_emotion_predictor',
    version='1.0.1',
    author='takenaka Yoichi',
    author_email='takenaka@kansai-u.ac.jp',  
    description='A DeBERTa-based emotion predictor for Japanese text.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://huggingface.co/YoichiTakenaka/deverta-v3-japanese-large-Joy',  
    packages=find_packages(),
    include_package_data=True,  # MANIFEST.in の内容も含める
    install_requires=[
        'torch',
        'transformers',
        'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)
