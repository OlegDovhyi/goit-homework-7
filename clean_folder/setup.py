from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='Very good code',
    author='Oleg Dovhyi',
    author_email='oleg.dovgyy@gmail.com',
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': ['clean_folder = clean_folder.clean:sort']}
)