from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    try:
        # Mengambil konten dari URL
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ekstraksi data tidak terstruktur: teks & gambar
        texts = [p.get_text(strip=True) for p in soup.find_all('p')]

        # Perbaiki URL gambar relatif menjadi absolut
        images = [urljoin(url, img['src']) for img in soup.find_all('img') if 'src' in img.attrs]

        return render_template(
            'index.html', 
            url=url, 
            texts=texts, 
            images=images
        )
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
