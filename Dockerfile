# Start from a core stack version
FROM jupyter/minimal-notebook:latest
# Install from requirements.txt file
COPY requirements.txt /tmp/
# Copy src dir
COPY src/ /tmp/src/
# Install lib
RUN conda install --yes --file /tmp/requirements.txt && \
  fix-permissions $CONDA_DIR && \
  fix-permissions /home/$NB_USER
# Set pythonpath
ENV PYTHONPATH /tmp/src/