Shortens long URLs

Option to give custom short code

Set expiry time (in minutes)

Expired links show error

Tech used
--------
Python

Flask

datetime, random, string

How to Run
------
Install Flask:
pip install flask

Run app:
python app.py

Go to:
http://localhost:5000

API
----
POST /shorturls – create short URL
Required: url
Optional: shortcode, validity

GET /<shortcode> – redirects to original URL



