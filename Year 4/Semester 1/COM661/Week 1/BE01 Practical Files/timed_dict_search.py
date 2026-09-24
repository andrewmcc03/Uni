import time

def time_execution(code):
	start = time.perf_counter()
	eval(code)
	run_time = time.perf_counter() - start
	return run_time

def add_word(this_collection, keyword, url):
	if keyword in this_collection:
		this_collection[keyword].append(url)
	else:
		this_collection[keyword] = [url]

def make_collection(all_words, size):
	this_collection = {}
	for i in range(size):
		add_word(this_collection, all_words[i], "dummyURL")
	return this_collection

def lookup(keyword, collection):
	if keyword in collection:
		return collection[keyword]
	else:
		return []

all_words = []
fin = open("words.txt")
for line in fin:
    word = line.strip()
    all_words.append(word)
fin.close()	

collection = make_collection(all_words, 1000)
print("Lookup for 1000 words")
print(time_execution("lookup('xxx', collection)"))

collection = make_collection(all_words, 2000)
print("Lookup for 2000 words")
print(time_execution("lookup('xxx', collection)"))

collection = make_collection(all_words, 4000)
print("Lookup for 4000 words")
print(time_execution("lookup('xxx',collection)"))

collection = make_collection(all_words, 8000)
print("Lookup for 8000 words")
print(time_execution("lookup('xxx', collection)"))

collection = make_collection(all_words, 16000)
print("Lookup for 16000 words")
print(time_execution("lookup('xxx', collection)"))
	
collection = make_collection(all_words, 32000)
print("Lookup for 32000 words")
print(time_execution("lookup('xxx', collection)"))