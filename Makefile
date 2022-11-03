STT_REPO ?= https://github.com/OM3GA-SOLUTIONS-d-o-o/daktilograf-STT.git
STT_SHA  ?= origin/main

Dockerfile%: Dockerfile%.tmpl
	sed \
		-e "s|#STT_REPO#|$(STT_REPO)|g" \
		-e "s|#STT_SHA#|$(STT_SHA)|g" \
		< $< > $@
