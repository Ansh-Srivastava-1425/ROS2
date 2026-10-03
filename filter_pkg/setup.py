import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'filter_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ansh',
    maintainer_email='kumar.ansh7591@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'temp_publisher = filter_pkg.temp_publisher:main',
            'filter_node = filter_pkg.filter_node:main',
            'display_sub = filter_pkg.display_sub:main',
        ],
    },
)