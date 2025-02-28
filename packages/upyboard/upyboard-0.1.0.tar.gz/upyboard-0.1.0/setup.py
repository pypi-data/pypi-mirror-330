from setuptools import setup, find_packages, Command

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='upyboard',
    version='0.1.0',
    description='This is a CLI management tool for MicroPython-based embedded systems.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chanmin.park',
    author_email='devcamp@gmail.com',
    url='https://github.com/planxstudio/upyboard',
    install_requires=['click', 'python-dotenv', 'pyserial', 'genlib', 'mpy-cross'],
    packages=find_packages(),
    keywords=['micropython', 'pyserial', 'genlib'],
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'upy = upy.upy:main',    
        ],
    },
)
