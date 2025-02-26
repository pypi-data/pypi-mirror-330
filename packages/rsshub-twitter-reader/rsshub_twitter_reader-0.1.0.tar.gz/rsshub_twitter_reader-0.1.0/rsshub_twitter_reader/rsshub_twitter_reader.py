import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re
import hashlib

__version__ = '0.0.4'

class RSSHubTwitterReader:
    """
    RSSHubTwitterReader
    ===================

    Este módulo permite a leitura de tweets via RSS utilizando o RSSHub.

    Funcionalidades:
    - Captura tweets de um usuário do X (antigo Twitter) informando o nome de usuário.
    - Remove URLs do título e retorna o link original em uma coluna separada.
    - Filtra tweets com base em palavras-chave fornecidas.
    - Obtém informações do canal, incluindo nome, descrição, link e última atualização.

    Dependências:
    - requests
    - pandas
    - lxml

    Exemplo de uso:

        from rsshub_twitter_reader import RSSHubTwitterReader

        rss_reader = RSSHubTwitterReader('einvestidor')
        tweets = rss_reader.fetch_rss()
        print(tweets)

        # Filtrar tweets com palavras-chave
        filtered_tweets = rss_reader.filter(['MRVE3', 'VBBR3'])
        print(filtered_tweets)

        # Obter informações do canal
        channel_info = rss_reader.get_info()
        print(channel_info)

    """

    def __init__(self, username):
        self.username = username
        self.url = f"https://rsshub.app/twitter/user/{username}"
        self.items = []
        self.channel_info = {}

    def fetch_rss(self):
        """Fetch and parse the RSS feed, returning parsed tweets."""
        response = requests.get(self.url)
        if response.status_code == 200:
            if 'Looks like something went wrong' in response.text:
                print("Error: Channel not found. No information available.")
                return None  # Return None if channel not found            
        else:
            print("Error in get chanel info. HttpStatus code: ", response.status_code)
            return None
        root = ET.fromstring(response.content)
        self.items = root.findall('.//item')
        return self._parse_items()

    def __parse_items(self):
        """Parse the RSS items and extract required fields."""
        data = []
        for item in self.items:
            title = item.find('title').text
            description=item.find('description').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            # Compute MD5 hash of the title
            md5_hash = hashlib.md5(title.encode('utf-8')).hexdigest()

            # Format date to yyyy-mm-dd hh:mm:ss
            date = pd.to_datetime(pub_date).strftime('%Y-%m-%d %H:%M:%S')

            # Clean title by removing HTML and emojis
            title = re.sub(r'<[^>]+>', '', title)  # Remove HTML tags
            title = re.sub(r'[𐀀-􏿿]+', '', title)  # Remove emojis mantendo acentos

            description = re.sub(r'<[^>]+>', '', description)  # Remove HTML tags
            description = re.sub(r'[𐀀-􏿿]+', '', description)  # Remove emojis mantendo acentos

            # Extract and remove URL from title
            original_link = re.search(r'https?://\S+', title)
            if original_link:
                original_link = original_link.group(0)
                title = re.sub(r'\s?https?://\S+', '', title)
            else:
                original_link = link                

            data.append({
                'title': title,
                'description': description,
                'link': link,
                'date': date,
                'original_link': original_link,
                'md5_hash_tweet': md5_hash
            })

        df = pd.DataFrame(data)
        return df

    def filter(self, keywords):
        """Fetch tweets and filter them based on a list of keywords."""
        df = self.fetch_rss()  # Fetch and parse tweets
        df['matchKeyword'] = df['title'].apply(
        lambda title: next((kw for kw in keywords if kw.lower() in title.lower()), None)
    )
        return df.dropna(subset=['matchKeyword'])

    def get_info(self):
        """Get channel information from the RSS feed."""
        response = requests.get(self.url)
        if response.status_code == 200:
            if 'Looks like something went wrong' in response.text:
                print("Error: Channel not found. No information available.")
                return None  # Return None if channel not found
            root = ET.fromstring(response.content)
        else:
            print("Error in get chanel info. HttpStatus code: ", response.status_code)
            return None        
        channel = root.find('.//channel')
        title = channel.find('title').text
        description = channel.find('description').text
        link = channel.find('link').text
        last_update = channel.find('lastBuildDate').text
        last_update = pd.to_datetime(last_update).strftime('%Y-%m-%d %H:%M:%S')

        self.channel_info = {
            'channelName': title,
            'description': description,
            'link': link,
            'last_update': last_update
        }
        return self.channel_info
