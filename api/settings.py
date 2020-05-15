import os

#environment
DB_URI = os.environ.get("DB_URI", "put local DB string here")
IS_PRODUCTION =  os.environ.get("IS_PRODUCTION", "false")

# auth related
CREATE_ACCOUNT_CODE = "SeniorDesignS2020"
JWT_SECRET =  os.environ.get("JWT_SECRET", "changeme")

#enumerations 
SOURCES = ["TWITTER", "NEWS", "NOAA", "USGS"]

# threat range in miles
THREAT_RANGE = 50

# email
SYSTEM_EMAIL_ADDRESS = os.environ.get("SYSTEM_EMAIL_ADDRESS", "Email")
SYSTEM_EMAIL_PW =  os.environ.get("SYSTEM_EMAIL_PW", "Password")
EMAIL_SERVER = os.environ.get("EMAIL_SERVER", "EMAIL_SERVER")
