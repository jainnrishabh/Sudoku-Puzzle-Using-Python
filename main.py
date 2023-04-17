from flask import Flask , render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
	return  render_template('puzzle_new.html')


if __name__ == "__main__":
    app.run()