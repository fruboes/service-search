FROM python:3.11

COPY build_data /build_data/

RUN pip install gunicorn
RUN /bin/bash -c "pip install ./build_data/*.whl"

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:8000 -w 4 'cc_service_search.app:app'


