## Process this file with automake to produce Makefile.in

ubuntuonlinetour_datadir = $(datadir)/applications
ubuntuonlinetour_data_in_files = ubuntu-online-tour.desktop.in
ubuntuonlinetour_data_DATA = $(ubuntuonlinetour_data_in_files:.desktop.in=.desktop)

ubuntuonlinetour_pixmapsdir = $(datadir)/pixmaps

ubuntuonlinetour_pixmaps_DATA = ubuntu-online-tour.png

@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST = $(ubuntuonlinetour_data_in_files)
DISTCLEANFILES = $(ubuntuonlinetour_data_in_files:.desktop.in=.desktop)

