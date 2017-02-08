#!/Users/grange/anaconda/bin/python
#    Copyright 2015 Yan Grange (grange@astron.nl), 
#    ASTRON, Netherlands institute for radio astronomy.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
   
import os, sys, datetime, certifi
import urllib3 as urllib

APOD_URL="https://apod.nasa.gov/apod"
APOD_HOME="APOD_pull"

APOD_HOME=os.environ['HOME']+"/"+APOD_HOME

IMEXTS=["jpg","gif","png","tif","tiff","jpeg"]

def imgext(a):
    for ext in IMEXTS:
        if ext in a.lower():
            return True
    return False

def imgstrip(c):
    if "image" in c:
        csp=c.split('"')
        for cc in csp:
            if "image" in cc:
                return APOD_URL+"/"+cc
    else:
        csp=c.split('"')
        for cc in csp:
            for ex in IMEXTS:
                if ex in cc:
                    if "http" in cc:
                        return cc
                    else:
                        return APOD_URL+"/"+cc
        prevdat=(datetime.date(int("20"+date[0:2]),int(date[2:4]),int(date[4:6]))-datetime.timedelta(1)).strftime("%y%m%d")
        return get_img(prevdat)

def ytstrip(c):
    for cc in c.split('"'):
        if "youtube.com" in cc:
            cout=cc
    flag=0
    for urp in cout.split("/"):
        if flag:
            ytur=urp.split("?")[0]
        elif urp == "v":
            flag=1
        elif urp == "embed":
            flag=1

    return "http://img.youtube.com/vi/"+ytur+"/0.jpg"

if len(sys.argv[1:]) == 1:
    date=sys.argv[1]
else:
    date=datetime.date.today().strftime("%y%m%d")

def get_img(date):
    baseurl=APOD_URL+"/"+"ap"+date+".html"
    http = urllib.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    hf=http.request('GET', baseurl, preload_content=False)
    if hf.status !=200:
        sys.stderr.write("Something went wrong. URL seems not to exist\n\n")
        sys.stderr.write(str(hf.status+"\n\n"))
        sys.exit(2)
    else:
        data = hf.readlines()
    hf.close()
    hf.release_conn()

    longdat=datetime.date(int("20"+date[0:2]),int(date[2:4]),int(date[4:6])).strftime("%Y %B %-d")

    flag=0

    content_type = hf.headers['Content-Type']
    encoding = [c.split("=")[1].strip() for c in content_type.split(";") 
                if 'charset=' == c.strip()[:len('charset=')]][0]
    container=list()
    for lin in data:
        lin=lin.decode(encoding)
        if flag:
            if "</center>" not in lin:
                container.append(lin.strip())
            else:
                flag=0
        if longdat==lin.strip():
            flag=1
    for c in container:
        if "href" in c.lower() and imgext(c.lower()):
            return imgstrip(c)
        elif "youtube" in c:
            return ytstrip(c)

    prevdat=(datetime.date(int("20"+date[0:2]),int(date[2:4]),int(date[4:6]))-datetime.timedelta(1)).strftime("%y%m%d")
    return get_img(prevdat)

im=get_img(date)
ext=im[-3:]

with open(APOD_HOME+"/"+"currentapod.jpg","wb") as fh:
    http = urllib.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    req = http.request('GET', im)
    fh.write(req.data)

