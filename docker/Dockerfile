FROM ubuntu:16.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:cwchien/gradle && apt-get update && apt-get install -y wget git python-pip graphviz openjdk-8-jdk groovy2 gradle maven pandoc ttf-freefont plantuml unzip && apt-get remove -y --purge pandoc && wget https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb && dpkg -i pandoc-1.19.2.1-1-amd64.deb && apt-get install -yf && pip install pandocfilters && pip install jinja2 && git clone https://github.com/att/MkTechDocs

# Install a slightly altered version of mktechdocs with PDF support removed
ADD mktechdocs-html-only MkTechDocs/bin/mktechdocs
ADD docker-entry.sh /

ENV MKTECHDOCSHOME /MkTechDocs
ENV PATH /bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/share/groovy2/bin:/MkTechDocs/bin:/MkTechDocs/bin/groovy:.
ENV PYTHONPATH /MkTechDocs/bin

ENTRYPOINT ["/docker-entry.sh"]

