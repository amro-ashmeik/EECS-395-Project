# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltkclean import clean
import pandas as pd

movie_links = {'Action': [], 'Comedy': [], 'Horror': []}
total_skipped = {'Action': 0, 'Comedy': 0, 'Horror': 0}
total = {'Action': 0, 'Comedy': 0, 'Horror': 0}

for genre in movie_links.keys():
	quote_page = 'https://www.imsdb.com/genre/{}'.format(genre)
	page = urlopen(quote_page)
	soup = BeautifulSoup(page, 'html.parser')

	all_movies = soup.find_all('table')[1].find_all('p')
	for p in all_movies:
		ref = p.find('a', href=True)
		ref = ref['href']
		ref = ref.rsplit('/', 1)[-1]
		ref = ref.rsplit(' ', 1)[0]
		ref = ref.strip().replace(" ", "-")
		movie_links[genre].append(ref)

data = []
for genre in movie_links:
	print('--------------{}-------------'.format(genre))
	for movielink in movie_links[genre]:
		total[genre] += 1

		if ':' in movielink:
			movielink = movielink.replace(':', '')

		print(movielink)
		quote_page = 'https://www.imsdb.com/scripts/{}.html'.format(movielink)
		try:
			page = urlopen(quote_page)
		except Exception as e:
			print(e, 'skipped {}'.format(movielink))
			continue
		soup = BeautifulSoup(page, 'html.parser')

		all_text = soup.find('pre')

		if not all_text:
			total_skipped[genre] += 1
			print('skipped not all_text', movielink)
			continue

		if all_text.find('pre'):
			print('got here')
			all_text = all_text.find_all('pre')[0]

		script = []
		for elem in all_text:
			if elem.name == 'b':
				continue
			script.append(elem.string)

		if not script:
			total_skipped[genre] += 1
			print('skipped not script', movielink)
			continue

		if None in script:
			total_skipped[genre] += 1
			print('skipped None in script', movielink)
			continue

		script = ' '.join(script)
		script = ' '.join(script.split())
		script = script.split(' ')
		cleaned_script, tokens = clean(script)

		if tokens < 1000:
			total_skipped[genre] += 1
			print('skipped < 1000 tokens', movielink)
			continue

		row = (movielink, genre, cleaned_script)
		data.append(row)


print(total, total_skipped)
df = pd.DataFrame(data, columns=('Movie', 'Genre', 'Script'))
df.to_csv('finaldata.csv', index=False)