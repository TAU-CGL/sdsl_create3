import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'sdsl_create3'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Michael Bilevich',
    maintainer_email='mickelbil84@gmail.com',
    description='iRobot Create3 launch/driver for SDSL',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'r3_horn = sdsl_create3.r3_horn:main',
            'sds_publisher = sdsl_create3.sds_publisher:main'
        ],
    },
)
