# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:06:32 2016

@author: dheepan.ramanan
"""

import httplib2
from bs4 import BeautifulSoup as bs

def realtime_request(project_name, modelName, verbatim):
    
    xml = """
   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:real="http://realtime.cbapi.clarabridge.com/">
  <soapenv:Header/>
  <soapenv:Body>
     <real:processMultiVerbatimDocument>
        <processMultiVerbatimDocumentRequest>
           <projectName>%s</projectName>
           <modelName>%s</modelName>
           <responseLevel>VERBATIM_AND_SENTENCE</responseLevel>
           <save>false</save>
           <verbatimSet>
              <verbatim type="RESPONSE_TEXT">%s</verbatim>
           </verbatimSet>
        </processMultiVerbatimDocumentRequest>
     </real:processMultiVerbatimDocument>
  </soapenv:Body>
</soapenv:Envelope>
    """% (project_name, modelName, verbatim)
    
  
    #Create HTTP request
    h = httplib2.Http()
    h.add_credentials('dheepan.dexter', 'Recalitrantkitten5')
    resp, content = h.request('https://dexter.clarabridge.net:443/cbapi/realtime?wsdl', 
        "POST", body=xml, 
        headers={'content-type':'text/xml'} )   
    sentiment = bs(content,'lxml').degreesentiment.text
    return sentiment
				