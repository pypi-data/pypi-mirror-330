from setuptools import setup, find_packages

setup(
    name='teon',
    version='0.5.7',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'teon': [
            'level_editor/*',
            'level_editor/images/*',
            'level_editor/fonts/*',
            'extra/*',
            'icon.png',
        ],
    },
    install_requires=[
        'pygame',
        'pillow',
    ],
)
