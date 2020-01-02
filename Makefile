VERS = $(shell cat VERSION)

all:
	$(info nothing to build)

install:
	mkdir -p install_files/opt/mktechdocs
	cp -r bin lib docs install_files/opt/mktechdocs/.

version:
	$(info $(VERS))

##########################################################################################3
# Debian source package
#

debian_source:
	debuild -S

# mktechdocs_1.0.4ppa2_source.changes
dput:
	dput -f ppa:jsseidel/mktechdocs ../mktechdocs_$(VERS)_source.changes

