import os,sys,random

path=os.getcwd()


var = {'host': '10.10.110.17', 'port':'9000', 'scheme':'ws'}
"""
def getHtml(text):
	return text  % {'username': "User%d" % random.randint(0, 100), 'host': host, 'port': port, 'scheme': scheme}

def getJava(text):
	return text % {'username': "User%d" % random.randint(0, 100), 'host': host, 'port': port, 'scheme': scheme}
"""

def htmlHelper(temp):
	java = ""
	temp['username'] = "User%d" % random.randint(0, 100)
	temp['percent'] = '%'
	jfile=open(path+"/static/js"+"/gpio_test.js")
	jlines=jfile.readlines()
	jfile.close()
	for jline in jlines:
		java = java + jline

	style=""
	sfile=open(path+"/static/css"+"/style.css")
	slines=sfile.readlines()
	sfile.close()
	for sline in slines:
		style = style + sline

	html = ""
	hfile=open(path+"/static"+"/gpio_server.html")
	hlines=hfile.readlines()
	hfile.close()
	for hline in hlines:
		if hline.strip() == "</head>":
			html = html + style + java + hline
		else:
			html = html + hline
	#print html
	return html % temp

if __name__ == '__main__':
	
	print htmlHelper(var)


