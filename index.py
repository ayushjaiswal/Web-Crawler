def splitwords(source):
	splitlist=" ,<.>/?\"\:;}][{\\|+=_-)(\n!"
	words=[]
	word=''
	for ch in source:
		if ch in splitlist:
			if len(word) != 0:
				words.append(word)
				word=''
		else:
			word=word+ch
	if len(word) != 0:
		words.append(word)
	return words

def add_to_index(index,keyword,url):
    flag = 0
    for entry in index:
        if entry[0] == keyword:
            if url not in entry[1]:
                entry[1].append(url)
            flag=1
            break
    if len(index) == 0 or flag == 0:
        p=[]
        q=[]
        q.append(url)
        p.append(keyword)
        p.append(q)
        index.append(p)

def add_page_to_index(index,url,content):
    words=splitwords(content)
    for word in words:
        add_to_index(index,word,url)
        
def lookup(index, keyword):
	for entry in index:
		if entry[0] == keyword:
			return entry[1]
	return []
