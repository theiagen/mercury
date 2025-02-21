ARG MERCURY_VER="1.1.0-dev"

FROM google/cloud-sdk:480.0.0-slim

ARG MERCURY_VER

LABEL base.image="google/cloud-sdk:480.0.0-slim"
LABEL software="mercury"
LABEL software.version=${MERCURY_VER}
LABEL description="Mercury_Prep_N_Batch"
LABEL website="https://github.com/theiagen/mercury"
LABEL license="https://github.com/theiagen/mercury/blob/main/LICENSE"
LABEL maintainer="Sage Wright"
LABEL maintainer.email="sage.wright@theiagen.com"

ARG DEBIAN_FRONTEND=noninteractive

# Tell gcloud to save state in /.config so it's easy to override as a mounted volume.
ENV HOME=/

# install stuff via apt; cleanup apt garbage
RUN apt-get update && apt-get install -y --no-install-recommends \
 ca-certificates \
 wget \
 python3 \
 python3-pip \
 python3-setuptools \
 gawk \
 git && \
 apt-get autoclean && rm -rf /var/lib/apt/lists/*

# clone broad/terra-tools repo
# copying scripts dir to `/scripts` for consistency
# make all scripts within /scripts exectuable to all users
RUN git clone https://github.com/broadinstitute/terra-tools.git && \
 mkdir /scripts && \
 cp -vr /terra-tools/scripts/* /scripts && \
 chmod +x /scripts/*

# we are installing updated versions of each of the following via pip3/pypi:
RUN pip3 install --break-system-packages firecloud \
google-auth-httplib2 \
gcs-oauth2-boto-plugin \
google-api-python-client \
google-cloud-storage \
google-cloud-bigquery \
pandas \
tqdm \
numpy 

ENV LC_ALL=C

# copy in all of the mercury code
#RUN wget https://github.com/theiagen/mercury/archive/refs/tags/v${MERCURY_VER}.tar.gz && \
 #  tar -xzvf v${MERCURY_VER}.tar.gz && \
  # mv -v mercury-${MERCURY_VER} /mercury

RUN git clone -b kzm-mercury-dev https://github.com/theiagen/mercury.git

# final working directory is /data
WORKDIR /data

# put broadinstitute/terra-tools & mercury scripts onto the PATH
ENV PATH=${PATH}:/scripts:/mercury/mercury

# check that we have stuff installed
RUN gcloud storage --help && pip3 list && mercury.py --help