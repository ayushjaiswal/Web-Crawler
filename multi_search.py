def multi_lookup(index, query):
	urls=[]
	p={}
	for word in query:
		if word not in index:
			return []
		entries=lookup(index,word)
		for entry in entries:
			if entry[0] in p:
				p[entry[0]].append(entry[1])
			else:
				p[entry[0]]=[entry[1]]
	for url in p:
		found=1
		for i in range(1,len(p[url])):
			if p[url][i]-p[url][i-1]!=1:
				found=0
				break
		if found == 1 and url not in urls:
			urls.append(url)
	return urls
		


def crawl_web(seed): # returns index, graph of inlinks
	tocrawl = [seed]
	crawled = []
	graph = {}  # <url>, [list of pages it links to]
	index = {} 
	while tocrawl: 
		page = tocrawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page] = outlinks
			union(tocrawl, outlinks)
			crawled.append(page)
	return index, graph


def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1: 
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1:end_quote]
	return url, end_quote

def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links


def union(a, b):
	for e in b:
		if e not in a:
			a.append(e)

def add_page_to_index(index, url, content):
	words = content.split()
	i=0
	for word in words:
		add_to_index(index, word, i, url)
		i+=1
		
def add_to_index(index, keyword, pos, url):
	if keyword in index:
		index[keyword].append([url, pos])
	else:
		index[keyword] = [[url, pos]]

def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None
