from flask import Flask, render_template, jsonify
from portfolio import Portfolio
from config import Config

app = Flask(__name__)

@app.route("/")
def index():
    """Render the portfolio dashboard."""
    portfolio = Portfolio()
    summary = portfolio.get_portfolio_summary()
    holdings = portfolio.get_holdings().to_dict(orient="records")
    positions = portfolio.get_positions().to_dict(orient="records")
    return render_template("index.html", summary=summary, holdings=holdings, positions=positions)

@app.route("/api/portfolio")
def api_portfolio():
    """Provide portfolio data as JSON."""
    portfolio = Portfolio()
    summary = portfolio.get_portfolio_summary()
    holdings = portfolio.get_holdings().to_dict(orient="records")
    positions = portfolio.get_positions().to_dict(orient="records")
    return jsonify({"summary": summary, "holdings": holdings, "positions": positions})

if __name__ == "__main__":
    Config.validate()
    if Config.load_saved_session():
        app.run(debug=True)
    else:
        print("Failed to load session. Please authenticate first.")
