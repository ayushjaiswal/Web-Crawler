def get_page(url):
	try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return ""

def union(p,links):
	for x in links:
		if x not in p:
			p.append(x)
		
def get_all_links(page):
	p=[]
	idx=page.find("href=")
	while idx != -1:
		startlink=page.find("\"",idx)
		endlink=page.find("\"",startlink+1)
		startlink=startlink+1
		if page.find("http",startlink) != -1:
			p.append(page[startlink:endlink])
		else:
			j = len(p)-1
			while j>=0 and p[j].find("http") == -1:
				j=j-1
			if j>=0:
				p.append(p[j]+page[startlink:endlink])
		#if p[len(p)-1].find("more") != -1:
		#	print p[len(p)-1]
		page=page[endlink:]
		idx=page.find("href=")
	return p

def crawl_web(seed):
	limit=10 # no. of pages to crawl, else will go infinitely
	tocrawl=[seed]
	crawled=[]
	ind=[] #index
	i=0
	while i<len(tocrawl) and limit>0: #limit added
		page=tocrawl[i]
		i=i+1
		if page not in crawled:
			limit=limit-1 # limit
			print page # check
			content=get_page(page)
			import index
			index.add_page_to_index(ind, page, content) #contained in index.py
			union(tocrawl,get_all_links(content))
			crawled.append(page)
	return ind
