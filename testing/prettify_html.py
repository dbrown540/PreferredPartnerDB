from bs4 import BeautifulSoup

with open('testing//new.html', 'r', encoding='utf-8') as experiences_file:
    danny_content = experiences_file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(danny_content, 'lxml')

# Prettify the HTML content
prettified_html = soup.prettify()

with open('testing//new.html', 'w', encoding='utf-8') as newfile:
    writer = newfile.write(prettified_html)
    