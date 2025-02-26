import os
from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")


setup(
    name='keras-model-hub',
    packages=['keras_model_hub'],
    description="Model hub for Pytorch.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.8',
    install_requires=[
        "keras>=2.0.0",
    ],
    url='https://gitee.com/summry/keras-model-hub',
    author='summy',
    author_email='fkfkfk2024@2925.com',
    keywords=['keras', 'AI', 'Machine learning', 'Deep learning', 'tensorflow', 'model', 'hub'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)

