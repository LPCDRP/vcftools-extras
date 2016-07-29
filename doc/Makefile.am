
PANDOC = @PANDOC@

#EXTRA_DIST = vcf-consenpos.1.md

if HAVE_PANDOC
man_MANS = vcf-consenpos.1
endif

%.1: %.1.md
	$(PANDOC) -s --from=markdown --to=man $< > $@

clean-local:
	$(RM) $(man_MANS)
