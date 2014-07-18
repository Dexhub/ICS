from bs4 import BeautifulSoup

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b
print type(tag)
print type(tag.name)
tag.name = "blockquote"
print tag.attrs
