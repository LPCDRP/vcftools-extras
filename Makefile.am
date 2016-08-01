
PANDOC = @PANDOC@

SUBDIRS = src doc test

EXTRA_DIST = $(srcdir)/test/data/*.vcf
#INSTALL INSTALL.md LICENSE

# Convert markdown documentation to true plain text
# (no matter how much you try, markdown source won't really be as readable as formatted plain text)
INSTALL: INSTALL.md
	$(PANDOC) -t plain $< -o $@

clean-local:
	$(RM) INSTALL
