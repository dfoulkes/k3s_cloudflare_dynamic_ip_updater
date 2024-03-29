FROM python:3.11-slim
COPY ./dist/cloudflareupdateip-0.1.0-py3-none-any.whl /tmp/dist/cloudflareupdateip-0.1.0-py3-none-any.whl
RUN pip install /tmp/dist/cloudflareupdateip-0.1.0-py3-none-any.whl
CMD ["cfcli", "update"]