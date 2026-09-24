url = input("Enter a full URL: ").strip()

protocol_end = url.find("://")
if protocol_end != -1:
	protocol = url[:protocol_end]
	remainder = url[protocol_end + 3:]
else:
	protocol = ""
	remainder = url

query_start = remainder.find("?")
if query_start != -1:
	query_string = remainder[query_start + 1:]
	remainder = remainder[:query_start]
else:
	query_string = ""

path_start = remainder.find("/")
if path_start != -1:
	domain = remainder[:path_start]
	path = remainder[path_start:]
else:
	domain = remainder
	path = ""

print(f"\nURL: {url}")
print("======================================================================================================")
print(f"Protocol: {protocol}")
print(f"Domain: {domain}")
print(f"Path: {path}")
print(f"Query string: {query_string}")

for parameter in query_string.split("&"):
	if parameter:
		separator = parameter.find("=")
		if separator != -1:
			name = parameter[:separator]
			value = parameter[separator + 1:]
		else:
			name = parameter
			value = ""
		print(f"{name} = {value}")

print("\n")