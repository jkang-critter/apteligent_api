Getting Started:

To get started with the scripts, please open the credentials.py file in the 'conf' directory. In the credentials.py file, please enter your Apteligent login email, password, and Oauth Token where it is specified. The Oauth Token can be found/generated in the Portal by navigating to User Settings and then the Oauth Tokens tab.

Once you have entered your credentials and saved the file, please make sure that you are in the 'apteligent_api' directory. From the command line, run 'python script_name' where script_name is error_monitoring.py or performance_management.py.

Customizing the Script:

The scripts are currently designed to pull all metrics for all app IDs. To pull a specific metric, please go to the appropriate script and comment out any metrics that are not relevant.


Troubleshoot:
If you are receiving the error message, "AttributeError: 'module' object has no attribute 'disable_warnings'", please run the following line:

pip install --upgrade requests
