What is PizzaPy?
---------------------

This program requires a running Postgresql database server, so it cannot be directly run without a well-configured Postgres server.



Requirements to run PizzaPy
-------------------------------

2. Create a virtual environment with python 3.10+ that contains dependency libraries in requirements.txt
    $ python3 -V
    (mac mini) $ cd /opt/github/pizza_project
    (mac mini) $ pvenv
    (mac mini) $ cd /opt/github/pizza_project/pizzapy
    (mac mini) $ pipr


4. Add batterypy and dimsumpy (custom libraries by Chris) at virtual environment's site-packages folder:
   
    $ cd /opt/github/pizza_project/venv/lib/python3.13/site-packages

    $ ln -s /opt/github/pizza_project/dimsumpy dimsumpy

    $ ln -s /opt/github/pizza_project/batterypy batterypy

6. Test run pizzapy CLI

    (venv) $ cd /opt/github/pizza_project

    (venv) $ py -m pizzapy.cli




2. a running Postgresql Server

3. a database connection file at local machine (mac or linux): /etc/config.json

8. Linux or MacOS (Windows requires changing config.json file location source code) 



LOCAL MAC ENV VARIABLES FOR POSTGRES SERVER CONNECTION
======================================================

Q: Where is database connection variable code in pizzapy?

    /opt/github/pizza_project/pizzapy/database_update/postgres_connection_model.py

Q: How to make pg env variables in local mac ~/prompts.sh?

    export PGHOST='o1.220122.COM'
    export PGPORT=5432
    export PGDATABASE='mydb'
    export PGUSER='postgres'
    export PGPASSWORD='hP'



REMOTE O1 POSTGRESQL SERVER
===========================

2. Check if postgresql service is active in firewalld.
    
    # firewall-cmd --list-all     (fls)

4. Check if postgres docker container is running

    $ docker ps -a    (psa)


Q: HOW TO RUN POSTGRES SERVER BY DOCKER?

    (o1) $ cd /opt/composes/pg17
    (o1) $ docker compose down && docker compose pull   (update the image)
    (o1) $ docker compose up -d


