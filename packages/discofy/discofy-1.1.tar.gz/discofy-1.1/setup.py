from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='discofy',
  version='1.1',
  description='Discofy allows control of Spotify playback through Discord API, offering features like play/pause, track skipping, volume control, and device management.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Echopixel',
  author_email='echopixel@proton.me', 
  classifiers=classifiers,
  license='CC BY-SA 4.0',
  keywords='spotify', 
  packages=find_packages(),
  install_requires=[''],
  extras_require={
      "dev" : ["pytest>=7.0", "twine>=4.0.2"],
  },
)