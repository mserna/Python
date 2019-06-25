# SkySat

__NOTE__ This service requires python3 to run

To run application:
- Unzip folder
- cd into skysat
- Make sure email addresses are entered in config.ini file
- Run command: python discover_sky_sat.py

To test application and classes:
- cd into skysat
- Run command: pytest -v


Files:
- discover_sky_sat.py = main class file
- alert_api.py = creates the json schema and also sends post request
- send_email.py = creates chart graph, grabs contact information and sends out email
- config.ini = configuration file that user can modify
- test_skysat.py = testfile that tests functionality of service
- screenshot = showing test run


Modules:
- schedule
- gviz_api
- pygooglechart
