
dist_bin_SCRIPTS = vcf-combine-variants
bin_PROGRAMS = vcf-consenpos

vcf_consenpos_SOURCES = vcf-consenpos.py
vcf-consenpos$(EXEEXT): $(vcf_consenpos_SOURCES)

SUFFIXES =

SUFFIXES += $(EXEEXT) .py
.py$(EXEEXT):
	cp $< $@ && chmod +x $@

