#!/bin/sh

DISTDIR="./dist"
VERSION=`python3 setup.py --version`

echo "Creating release for ${VERSION}"

rm -r ${DISTDIR}
mkdir -p ${DISTDIR}
DISTDIR=`realpath ${DISTDIR}`
python3 setup.py sdist bdist_wheel

echo "Signing everything in ${DISTDIR}"
for _file in `ls -1 ${DISTDIR}`; do
	(cd ${DISTDIR} && gpg --detach-sign -a "${_file}")
done

twine upload dist/*
git push
git tag -s ${VERSION}
git push --tags
