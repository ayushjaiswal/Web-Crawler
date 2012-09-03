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
	if keyword in index:
		if url not in index[keyword]:
			index[keyword].append(url)
	else:
		index[keyword]=[url]

def add_page_to_index(index,url,content):
    words=splitwords(content)
    for word in words:
        add_to_index(index,word,url)
        
def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	return None
