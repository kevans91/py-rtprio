#!/bin/sh

DISTDIR=`realpath ./dist`

rm -r ${DISTDIR}
python3 setup.py sdist bdist_wheel

for _file in `ls -1 ${DISTDIR}`; do
	(cd ${DISTDIR} && gpg --detach-sign -a "${_file}")
done

twine upload dist/*
