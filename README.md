What is PizzaPy?
---------------------
PizzaPy is an standalone data program built by Chris Sze. This program requires a running Postgresql database server, so it cannot be directly run without a well-configured Postgres server.

Requirements to run PizzaPy
-------------------------------
1. a virtual environment with python 3.10+ that contains dependency libraries in requirements.txt
2. a running Postgresql Server
3. a database connection file at local machine (mac or linux): /etc/config.json
4. dimsumpy (custom library by Chris) at virtual environment's site-packages
   
    pizzapy/ven/lib/python3.11/site-packages/dimsumpy
   
6. batterypy (custom library by Chris) at virtual environment's site-packages
   
    pizzapy/ven/lib/python3.11/site-packages/batterypy
   
8. Linux or MacOS (Windows requires changing config.json file location source code) 

sample /etc/config.json file for Postgres DB Server
-----------------------------------------------
{
"POSTGRES_DB": "dbname",
"POSTGRES_USER": "my_username",
"POSTGRES_PASS": "my_password",
"POSTGRES_HOST": "1.2.3.4",
"POSTGRES_PORT": 5432
}

Contact
-------------
please contact me at 3chris at gmail.com for further questions.
