from flask import Flask, render_template, request, send_file, flash, redirect
from flask import Markup
from lxml import etree
import requests
import uuid


app = Flask(__name__)
app.secret_key = 'super-secret-key'

file_ext = "_sitemap_urls.csv"
file_name = str(uuid.uuid1())+str(file_ext)


@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        url_in = request.form
        print(url_in)
        if url_in is not None:
            input_url = url_in['url']
            r = requests.get(input_url)
            if r.status_code == 200:
                root = etree.fromstring(r.content)
                for sitemap in root:
                    children = sitemap.getchildren()
                    urls = children[0].text
                    with open(file_name, 'a+') as f:
                        f.write(f'{urls}\n')
                # return render_template("download.html", url_in=url_in)
                return redirect('download')
            else:
                flash("Bad url...Kindly Enter a valid url.")
                return render_template("index.html", url_in=url_in)
        else:
            flash("Kindly Enter url.")
            return render_template("index.html", url_in=url_in)
    else:
        return render_template("index.html")

    


@app.route('/download')
def download():
    return send_file(file_name, as_attachment=True)



# error handling

@app.errorhandler(404)
def error404(error):
    flash("Page Not found.", 'info')
    return render_template('index.html'), 404

@app.errorhandler(403)
def error403(error):
    flash("Something bad happened", 'info')
    return render_template('index.html'), 403


@app.errorhandler(500)
def error500(error):
    flash("Kindly enter a valid url", 'info')
    return render_template('index.html'), 500




if __name__ == '__main__':
    app.run(debug=True)