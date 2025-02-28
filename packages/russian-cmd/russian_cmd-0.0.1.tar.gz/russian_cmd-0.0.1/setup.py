from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='russian_cmd',
  version='0.0.1',
  author='nothingdev',
  author_email='anisimovd519@gmail.com',
  description='This is a fun module with some russian commands',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='russian cmd',
  python_requires='>=3.6'
)