
PANDOC = @PANDOC@

SUBDIRS = src doc

#EXTRA_DIST = INSTALL INSTALL.md LICENSE

# Convert markdown documentation to true plain text
# (no matter how much you try, markdown source won't really be as readable as formatted plain text)
INSTALL: INSTALL.md
	$(PANDOC) -t plain $< -o $@

clean-local:
	$(RM) INSTALL
