from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
  name='disnake_dyn_components',
  version='0.2.2',
  author='Lord_Nodus',
  author_email='LordNodus@mail.ru',
  description='Library for quick creation of ui components of discord with the ability to pass additional parameters',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/NodusLorden/DisnakeDynComponents',
  packages=find_packages(),
  install_requires=['disnake>=2.10.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='disnake discord bot buttons modals selectmenu',
  project_urls={
    'GitHub': 'https://github.com/NodusLorden/DisnakeDynComponents'
  },
  python_requires='>=3.12'
)
