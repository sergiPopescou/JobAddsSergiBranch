import re
import codecs
from tools import flags, assign_if_found


def label_value_regex(label):
    return re.compile(
        '<span class="jobAdLabel">%s: </span>'
        '<span class="jobAdValue">([^<]*)</span>' % label,
        flags=flags)
        
companyRegex = re.compile(
    '<h2 class="hidden-sm hidden-md hidden-lg hidden-xl"><a href="/">([^<]*)</a></h2>',
    #'<h2 class="hidden-sm hidden-md hidden-lg hidden-xl"><a href="([^<]*)</a></h2>',
    flags=flags)
companyRegexSec = re.compile(
    #'<h2 class="hidden-sm hidden-md hidden-lg hidden-xl"><a href="/">([^<]*)</a></h2>',
    '<h2 class="hidden-sm hidden-md hidden-lg hidden-xl"><a href="([^<]*)</a></h2>',
    flags=flags)
companyRegexSecAgain = re.compile('">([\s\S]*)',flags=flags)

titleRegex = re.compile('<title>AU job- og projektbank - Opslag: ([^<]*)</title>', flags=flags)
textRegex = re.compile('<div itemprop="description" class="jobDescriptionLimited">([\s\S]*)<\/div><p id="jobHomeLink"', flags=flags)

#industryRegex = "Education" #since AU DK is Arhus university
categoryRegex = re.compile('<ul class="jobKategori" title="Uddannelse">([\s\S]*)</ul><h3', flags=flags)#label_value_regex("Industri")
subcategoryRegex =  re.compile('<ul class="jobKategori" title="Arbejdsomrade">([\s\S]*)</ul></div>', flags=flags)#label_value_regex("Underkategori")
cityRegex = re.compile('<ul class="jobKategori" title="Geografi">([\s\S]*)</ul></div><div', flags=flags)#label_value_regex("Arbeidssted")
cityRegexSec = re.compile('<ul class="jobKategori" title="Geografi">([\s\S]*)</ul><h3>', flags=flags)#label_value_regex("Arbeidssted")
positioncodeRegex = re.compile('\(id #([0-9]*)\)">',flags=flags)#label_value_regex("Ref. Nr.")
dateRegex = re.compile('<span itemprop="datePosted">([^<]*)</span>',flags=flags)#label_value_regex("Publisert")


def jobBankAuDk(text, row):
    row["source"] = "jobbank.au.dk"

    assign_if_found(row, "jobtitle", titleRegex, text)

    data = {"industry": "Education", "category": None, "subcategory": None}#industry = "Education" #since AU DK is Arhus university
    #assign_if_found(data, "industry", industryRegex, text)
    assign_if_found(data, "category", categoryRegex, text)
    assign_if_found(data, "subcategory", subcategoryRegex, text)

    if data["subcategory"] is None:
        row["category"] = data["category"]
    else:
        row["category"] = "{category} : {subcategory}".format(**data)

    assign_if_found(row, "companyname", companyRegex, text)
    
    if row["companyname"] == None:
        assign_if_found(row, "companyname", companyRegexSec, text)
        if row["companyname"] != None:
            assign_if_found(row, "companyname", companyRegexSecAgain, row["companyname"])

    if not row["companyname"] and data["industry"] == "AU Jobbank":
        row["companyname"] = "AU Jobbank"
    # Note: Manpower group members have generic names such as
    # "Engineering", "IT" or "Finance".
    # If the full name is needed, an exception list could be built here
    # by examining each logo by hand.

    assign_if_found(row, "city", cityRegex, text)
    if row["city"] == None:
        assign_if_found(row, "city", cityRegexSec, text)
    assign_if_found(row, "positioncode", positioncodeRegex, text)
    assign_if_found(row, "date", dateRegex, text)
    assign_if_found(row, "text", textRegex, text)
    # postal address and zip code is not available

    return row


filenames = ["r5752611.html","r5752623.html","r5752624.html","r5752626.html",
"r5752627.html","r5752628.html","r5752629.html","r5752630.html","r5752634.html"]
for filename in filenames:
    with codecs.open("D:\\elance\\NoJob\\2014\\"+filename, "r") as HTML_File:
        text = "\n".join(HTML_File.readlines())

    # Structure of row
    row = {"category": None, "filename": None, "url": None, "jobtitle": None,
           "companyname": None, "zipcode": None, "city": None, "source": None,
       "date": None, "text": None, "positioncode": None}
    row = jobBankAuDk(text,row)
    print "Filename\t:\t"+filename
    for key in row:
        print key,":", row[key]
    print "---------------------------------------------------"
#print row
