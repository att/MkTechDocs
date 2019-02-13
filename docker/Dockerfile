FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && apt-get install -y wget git python3-pip graphviz openjdk-8-jdk groovy gradle maven pandoc plantuml unzip && pip3 install pandocfilters jinja2 && git clone https://github.com/att/MkTechDocs

# Update the alternatives to use java 8 JRE
RUN update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

# Add a flag file so that mktechdocs can error out about PDF building if it
# finds that its in a docker environment
ADD dockerflag /
ADD docker-entry.sh /

ENV MKTECHDOCSHOME /MkTechDocs
ENV PATH /bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/share/groovy2/bin:/MkTechDocs/bin:/MkTechDocs/bin/groovy:.
ENV PYTHONPATH /MkTechDocs/bin

ENTRYPOINT ["/docker-entry.sh"]

