FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && apt-get install -y wget git python3-jinja2 python3-pandocfilters graphviz openjdk-8-jdk groovy gradle maven pandoc plantuml unzip && git clone https://github.com/att/MkTechDocs && wget https://github.com/jsseidel/groovy-pandoc/releases/download/v0.8/GroovyPandoc-0.8.jar -O /MkTechDocs/lib/GroovyPandoc-0.8.jar

# Update the alternatives to use java 8 JRE
RUN update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

# Add a flag file so that mktechdocs can error out about PDF building if it
# finds that its in a docker environment
RUN echo 1 > /MkTechDocs/nopdf
ADD docker-entry.sh /

ENV MKTECHDOCSHOME /MkTechDocs
ENV PATH /bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/share/groovy2/bin:/MkTechDocs/bin:/MkTechDocs/bin/groovy:.
ENV PYTHONPATH /MkTechDocs/bin

ENTRYPOINT ["/docker-entry.sh"]

