import matplotlib.pyplot as plt
import io
import urllib, base64
import urllib.request
from PIL import Image

'''
def test():
	plt.plot(range(10))
	fig = plt.gcf()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = 'data:image/png;base64,' + urllib.parse.quote(string)
	html = '<img src = "%s"/>' % uri
	return html
'''

def test():
	url = "https://www.python.org/static/img/python-logo@2x.png"
	img_in = urllib.request.urlopen(url).read()
	img_bin = io.BytesIO(img_in)
	img = Image.open(img_bin)
	html = img.save("logo.png","PNG")
	return html