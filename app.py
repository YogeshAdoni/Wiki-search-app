from flask import Flask, request, render_template, flash, redirect, url_for
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        search = request.form.get("search")
        
        # Input validation
        if not search:
            flash("Please enter a search term.", "warning")
            return redirect(url_for('home'))

        try:
            result = wikipedia.summary(search, sentences=2)
            return render_template("result.html", search=search, result=result)
        except DisambiguationError as e:
            flash(f"Your search term '{search}' resulted in multiple results. Try being more specific.", "danger")
            return redirect(url_for('home'))
        except PageError:
            flash(f"No results found for '{search}'. Please try another term.", "danger")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
