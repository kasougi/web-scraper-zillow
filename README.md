# Zillow Web Scraper

A powerful and convenient tool for scraping data from a website www.zollow.com.

# Getting start
```python
pyhton3 main.py
```
# Features
The scraper can accept parameters for data collection

Example:
* Prce min-max
* Beds min-max
* Bathroom min-max
* Parks min-max
* Square Feet min-max
* Year Built min-max

These parameters are used to search

# Output

The output data is a `.csv` file
The file contains 30 fields, such as:

* url
* price
* overview
* Bedrooms
* Bathrooms
* square footage
* address
* city
* zip
* Full bathrooms
* Basement
* Flooring
* Hometype
* Heating
* Cooling
* Appliances
* Interior
* Parking
* Totalspaces
* Architecturalstyle
* Parkingfeatures
* Lot
* Otherpropertyinformation
* Typeandstyle
* Construction materials
* Foundation
* Roof
* Utility
* New construction
* Condition
* Annual Tax Amoun


# Required packages
```python
pip3 install fake_useragent
pip3 install bs4
pip3 install selenium
pip3 install lxml
```

