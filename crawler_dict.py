### get_page copied from lecture --> find out
### page is the url of the webpage

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
	limit=100 # no. of pages to crawl, else will go infinitely
	tocrawl=[seed]
	crawled=[]
	ind={} #index
	graph={}
	i=0
	while i<len(tocrawl) and limit>0: #limit added
		page=tocrawl[i]
		i=i+1
		if page not in crawled:
			limit=limit-1 # limit
			print page # check
			content=get_page(page)
			import index_dict
			index_dict.add_page_to_index(ind, page, content) #contained in index.py
			outlinks=get_all_links(content)
			if page in graph:
				graph[page]=graph[page]+outlinks
			else:
				graph[page]=outlinks
			union(tocrawl,outlinks)
			crawled.append(page)
	return ind, graph
	
def compute_ranks(graph):
	d = 0.8 # damping factor
	numloops = 10
	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages
	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1 - d) / npages
			u=0.0
			for x in graph:
				if page in graph[x]:
					u=u+ranks[x]
			u=u*d
			if len(graph[page])!=0:
				u=u/len(graph[page])
				newrank=newrank+u
			newranks[page] = newrank
		ranks = newranks
	return ranks


def ordered_search(index, ranks, keyword):
    if keyword not in index:
        return []
    p=index[keyword]
    p=quicksort(p,ranks)
    return p

def quicksort(ls,ranks):
    if len(ls)<=1:
		return ls
    i,ls=partition(ls,ranks)
    l=quicksort(ls[0:i],ranks)
    r=quicksort(ls[i+1:],ranks)
    return l+[ls[i]]+r
	
def partition(ls,ranks):
    pivot=ranks[ls[0]]
    l=[]
    r=[]
    for i in range(1,len(ls)):
        if ranks[ls[i]]>pivot:
            l.append(ls[i])
        else:
            r.append(ls[i])
    ls=l+[ls[0]]+r
    return len(l),ls
