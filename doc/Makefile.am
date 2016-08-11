
PANDOC = @PANDOC@

EXTRA_DIST = \
vcftools-extras.7.md \
vcf-consenpos.1.md

if HAVE_PANDOC
man_MANS = vcf-consenpos.1 vcftools-extras.7
endif

%.7: %.7.md
	$(PANDOC) -s --from=markdown --to=man $< > $@

%.1: %.1.md
	$(PANDOC) -s --from=markdown --to=man $< > $@

clean-local:
	$(RM) $(man_MANS)
