installdir = $(pkglibdir)/python/Plugins/Extensions/hs9510VFD/locale/nl/LC_MESSAGES

.po.mo:
	$(MSGFMT) -o $@ $<

BUILT_SOURCES = VFD-Icons.mo

dist_install_DATA = \
	VFD-Icons.po \
	VFD-Icons.mo
