#!/bin/sh

autoreconf --force -i -v    
intltoolize -c
aclocal
rm -rf autom4te.cache
curdir=$(pwd)
cd po; intltool-update -p --verbose
cd "${curdir}"
#cd po-html; intltool-update -p --verbose
#cd "${curdir}"
exit 0

