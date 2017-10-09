FROM jupyter/scipy-notebook

MAINTAINER Heinrich Hartmann <heinrich@heinrichhartmann.com>

USER root
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y\
    emacs \
    tmux \
    curl \
    less

# Give $NB_USER passwordless sudo
RUN printf "$NB_USER\tALL=(ALL)\tNOPASSWD: ALL" > /etc/sudoers.d/$NB_USER

USER $NB_USER

RUN pip install \
    jupyter_contrib_nbextensions \
    jupyter_nbextensions_configurator

RUN jupyter contrib nbextension install --user &&\
    jupyter nbextensions_configurator enable --user

ADD python-circonusapi ./
RUN cd python-circonusapi; python setup.py install

EXPOSE 9999

ADD notebook.sh ./
ADD cmd.sh ./

CMD ["./cmd.sh"]
