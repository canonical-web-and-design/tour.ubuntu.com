AC_INIT([ubuntu-online-tour], [0.1])
AM_INIT_AUTOMAKE
AC_CONFIG_SRCDIR([js/jquery.min.js])
AM_MAINTAINER_MODE

GETTEXT_PACKAGE=ubuntu-online-tour
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package.])
AC_PROG_INTLTOOL([0.23])

dnl Add the languages which your application supports here.
ALL_LINGUAS=`(cd "$srcdir/po" && ls *.po) | sed 's/\.po$//' | tr '\n' ' '`

AM_GLIB_GNU_GETTEXT

AC_OUTPUT([
Makefile
data/Makefile
po/Makefile.in
])

