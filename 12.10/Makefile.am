SUBDIRS = data po

LINGUAS = en zh-CN

EXTRA_DIST = css img js pie videos videoplayer.swf $(LINGUAS)

install-data-hook:
	cd translate-html ; python setup.py build ; python setup.py install --prefix ./build 
	cp -f translate-html/build/bin/translate-html translate-html/bin/ 
	python translate-html/bin/translate-html --translate
	mkdir -p $(DESTDIR)$(docdir)
	cp -a $(srcdir)/chromeless $(DESTDIR)$(docdir)
	cp -a $(srcdir)/css $(DESTDIR)$(docdir)
	cp -a $(srcdir)/img $(DESTDIR)$(docdir)
	cp -a $(srcdir)/js $(DESTDIR)$(docdir)
	cp -a $(srcdir)/pie $(DESTDIR)$(docdir)
	cp -a $(srcdir)/videos $(DESTDIR)$(docdir)
	for language in $(LINGUAS) ; do \
	   cp -a $(srcdir)/$$language $(DESTDIR)$(docdir) ; \
	done
	cp -a $(srcdir)/videoplayer.swf $(DESTDIR)$(docdir)

uninstall-hook:
	rm -rf $(DESTDIR)$(docdir)/css
	rm -rf $(DESTDIR)$(docdir)/img
	rm -rf $(DESTDIR)$(docdir)/js
	rm -rf $(DESTDIR)$(docdir)/pie
	rm -rf $(DESTDIR)$(docdir)/videos
	for language in $(LINGUAS) ; do \
	    rm -rf $(DESTDIR)$(docdir)/$$language ; \
	done
	rm -f $(DESTDIR)$(docdir)/videoplayer.swf
	rmdir $(DESTDIR)$(docdir)

