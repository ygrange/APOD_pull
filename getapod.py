#!/usr/bin/python
import os, sys, datetime, urllib

APOD_URL="http://apod.nasa.gov/apod"
APOD_HOME="apod"

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
	hf=urllib.urlopen(baseurl)
	if hf.getcode() !=200:
		sys.stderr.write("Something went wrong. URL seems not to exist\n\n")
		sys.stderr.write(str(hf.getcode())+"\n\n")
		sys.exit(2)
	else:
		data=hf.readlines()
	hf.close()

	longdat=datetime.date(int("20"+date[0:2]),int(date[2:4]),int(date[4:6])).strftime("%Y %B %-d")

	flag=0

	container=list()
	for lin in data:
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
urllib.urlretrieve(im,APOD_HOME+"/"+"currentapod.jpg")
