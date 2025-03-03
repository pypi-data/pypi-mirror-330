import setuptools
import json

with open('../package.json') as file:
  pkg = json.load(file)
with open('../.copr/copr-orchestrate/dist/info.json') as file:
  info = json.load(file)

pkgName=info['copr']['nameAndAcronym']
pkgVersion=info['copr']['version']
pkgUrl=pkg['repository']['url'].removeprefix('git+').removesuffix('.git')

with open('./copr/__info__.py', 'w') as f:
  f.write('pkgName = \'%s\'\n' % pkgName)
  f.write('pkgVersion = \'%s\'\n' % pkgVersion)
  f.write('pkgUrl = \'%s\'\n' % pkgUrl)

# see setup.cfg for metadata
setuptools.setup(
  name='copr.py',
  packages=setuptools.find_packages(),
  install_requires=[
    'jmespath',
  ],
  extras_require={
    'publish': [
      'twine',
    ],
    'test': [
      'pytest',
      'pytest-sugar',
    ],
  },
  version=pkgVersion,
  author=info['software']['authorsLong'],
  author_email=info['software']['authorsEmail'],
  description='A library to access the ' + info['copr']['nameAndAcronym'],
  long_description='file: README.md',
  long_description_content_type='text/markdown',
  license=info['software']['license'].replace(' ', '-'),
  url=pkgUrl,
  keywords=info['copr']['keywords'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3',
  ],
)
