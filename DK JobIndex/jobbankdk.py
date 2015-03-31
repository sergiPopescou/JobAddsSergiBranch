# -*- coding: utf-8 -*-
import re
import codecs
from tools import flags, assign_if_found, remove_html_tags

def substringBeforeString(data, string):
    sIndex = data.find(string)
    if sIndex != -1:
        return data[:sIndex]
    return data

companyRegex = re.compile( '<span itemscope="itemscope" itemprop="hiringOrganization" itemtype="http://schema.org/Organization"><span itemprop="name">([^<]*)</span></span>', flags=flags)
companyRegexSec = re.compile('<h2 class="hidden-sm hidden-md hidden-lg hidden-xl"><a href="([^<]*)</a></h2>', flags=flags)
companyRegexSecAgain = re.compile('">([\s\S]*)',flags=flags)        
companyRegexThird = re.compile('<div class="companyinfo"><p>([^<]*)',flags=flags)

titleRegex = re.compile('<title> Opslag: ([^<]*)</title>', flags=flags)
textRegex = re.compile('<div itemprop="description" class="jobDescriptionLimited">([\s\S]*)</div>', flags=flags)
textRegexSec = re.compile('<div itemprop="description">([\s\S]*)</div><div class="hidden">', flags=flags)

industryRegex = re.compile('<div class="textbox"><h1>Branche</h1><p>([^<]*)', flags=flags) 
categoryRegex = re.compile('<ul class="jobKategori" title="Uddannelse">([\s\S]*)</ul>', flags=flags)
categoryRegexSec = re.compile('<h1>Uddannelse</h1><ul class="jobKategori" title="Uddannelse">([\s\S]*)</ul></div><div class="textbox"><h1>Arbej', flags=flags)
subcategoryRegex =  re.compile('<ul class="jobKategori" title="Arbejdsområde">([\s\S]*)</ul>', flags=flags)
cityRegex = re.compile('<ul class="jobKategori" title="Geografi">([\s\S]*)</ul></div>', flags=flags)#
cityRegexSec = re.compile('<ul class="jobKategori" title="Geografi">([\s\S]*)</ul><h3>', flags=flags)##
positioncodeRegex = re.compile('#([0-9]*)\)',flags=flags)
positioncodeRegexFull = re.compile('\(id #([0-9]*)\)">',flags=flags)
dateRegex = re.compile('<span itemprop="datePosted">([^<]*)</span>',flags=flags)


def jobBankDk(text, row):
    row["source"] = "jobbank.dk"

    assign_if_found(row, "jobtitle", titleRegex, text)

    data = {"category": None, "subcategory": None}
   
    assign_if_found(data, "category", categoryRegex, text)
    if data["category"] != None:    
        data["category"] = substringBeforeString(data["category"], "</ul>")
        data["category"] = remove_html_tags(data["category"].replace("</li><li>", ", "))
    
        
    assign_if_found(data, "subcategory", subcategoryRegex, text)
    if data["subcategory"] == None:
        row["category"] = data["category"]
    else:
        data["subcategory"] = substringBeforeString(data["subcategory"], "</ul>")
        data["subcategory"] = remove_html_tags(data["subcategory"].replace("</li><li>", ", "))
        row["category"] = "{category} : {subcategory}".format(**data)

    assign_if_found(row, "companyname", companyRegex, text)    
    if row["companyname"] == None:
        assign_if_found(row, "companyname", companyRegexSec, text)
        if row["companyname"] != None:
            assign_if_found(row, "companyname", companyRegexSecAgain, row["companyname"])
    if row["companyname"] == None:
        assign_if_found(row, "companyname", companyRegexThird, text)

    assign_if_found(row, "city", cityRegex, text)
    if row["city"] == None:
        assign_if_found(row, "city", cityRegexSec, text)
    if row["city"] != None:
        row["city"] = substringBeforeString(row["city"], "</ul>")
        row["city"] = remove_html_tags(row["city"].replace("</li><li>", ", "))

    if(row["jobtitle"] != None):
        assign_if_found(row, "positioncode", positioncodeRegex, row["jobtitle"])
    if(row["positioncode"] == None):
        assign_if_found(row, "positioncode", positioncodeRegexFull, text)
        
    assign_if_found(row, "date", dateRegex, text)
    assign_if_found(row, "text", textRegex, text)
    if(row["text"] == None):
        assign_if_found(row, "text", textRegexSec, text)
    if(row["text"] != None):
        row["text"] = substringBeforeString(row["text"], "</div>")

    return row
