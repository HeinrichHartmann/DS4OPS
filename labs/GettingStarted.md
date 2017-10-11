# Setup Tools

1. Setup Strigo
   - Log into this Strigo event: https://app.strigo.io/event/jXg874QKpTCRkoWcX
   - This will give you access to a personal VM in AWS, that we will use in this tutorial.

2. Setup Circonus
   - Create a Circonus account: https://login.circonus.com/signup
   - And provision the strigo VM with a monitoring agent

3. Setup Python Stack:
   - Install docker
     ```
     curl http://get.docker.com/  | sudo bash
     ```
   - Pull this repository from github
     ```
     git pull https://github.com/HeinrichHartmann/DataScience4Ops
     ```
   - Read through Dockerfile and docker.sh
   - Bootstrap work environment:
     ```
     sudo ./docker.sh --create
     ```
   - Run work environment: `suod ./docker.sh --run`
