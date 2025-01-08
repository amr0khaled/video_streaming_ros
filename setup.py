from setuptools import find_packages, setup

package_name = 'video_stream'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='amr0khaled',
    maintainer_email='amr0khaled0x@gmail.com',
    description='Streaming_Video',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pub = video_stream.pub:main',
            'sub = video_stream.sub:main'
        ],
    },
)
