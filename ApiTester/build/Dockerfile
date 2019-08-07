# Base Image
FROM storage-shshukun:5050/cta_base_env:latest as build

MAINTAINER shukun

ADD ./medicalbrain-cta-srv /opt/medicalbrain-cta-srv
WORKDIR /opt/medicalbrain-cta-srv
RUN rm -rf .venv && virtualenv .venv && \
    /opt/medicalbrain-cta-srv/.venv/bin/pip3 install -i https://mirrors.aliyun.com/pypi/simple pbr && \
    /opt/medicalbrain-cta-srv/.venv/bin/pip3 install -i https://mirrors.aliyun.com/pypi/simple sqlalchemy-migrate==0.11.0 && \
    /opt/medicalbrain-cta-srv/.venv/bin/pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt && \
    /opt/medicalbrain-cta-srv/.venv/bin/pip3 install -i http://103.211.47.132:3141/simple --trusted-host 103.211.47.132 --extra-index-url https://mirrors.aliyun.com/pypi/simple -r requirements_local.txt
RUN find /opt/medicalbrain-cta-srv/.venv -name '*.pyc' -delete
# 多阶段构建
FROM storage-shshukun:5050/cta_base_env:latest
COPY --from=build /opt/medicalbrain-cta-srv /opt/medicalbrain-cta-srv
WORKDIR /usr/bin
RUN ln -s /opt/medicalbrain-cta-srv/bin/run.sh run && \
    ln -s /opt/medicalbrain-cta-srv/.venv/bin/pip3 pip && \
    ln -s /opt/medicalbrain-cta-srv/.venv/bin/python3 python
WORKDIR /opt/medicalbrain-cta-srv
