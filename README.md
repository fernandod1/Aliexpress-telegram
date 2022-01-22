# Aliexpress to telegram post

Python script that reads Aliexpress offers urls from a Excel filename (.csv) and post then in a Telegram channel using a bot. You can see post design in image below. You need to create a cronjob in server to determine publishing frecuency of new offers.

-----------------------------
INSTALATION STEPS:
-----------------------------

1.) Open aliexpress.py

2.) Configure params of first lines.

3.) Create a cronjob entry in server with desired execution frecuency of script.

Example of cronjob entry for ejecuting script located in /home/ubuntu/ every 60 seconds:

* * * * * python3 /home/ubuntu/aliexpress.py > /home/ubuntu/log_aliexpress.log 2>&1

Output of script executed will be stored in /home/ubuntu/log_aliexpress.log for checking.

You can check more cronjobs entries examples in:
https://crontab.guru

Example screenshot of message published in Telegram Channel after execution:

<img src=screenshots/01.jpg>
