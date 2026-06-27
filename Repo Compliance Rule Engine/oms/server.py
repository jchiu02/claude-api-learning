from flask import Flask, jsonify, render_template

app = Flask(__name__)

PORTFOLIOS = [
    {
        "id": "sterling-ig",
        "name": "Sterling IG Fund",
        "bonds": [
            {
                "isin": "GB00BNGJJN71",
                "name": "UKT 0.125% 2026",
                "coupon": 0.125,
                "maturity_date": "2026-01-30",
                "positions": [
                    {"type": "bond", "notional": 50_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -15_000_000, "counterparty": "Barclays", "repo_maturity_t": 2},
                    {"type": "repo", "notional": -10_000_000, "counterparty": "JPM", "repo_maturity_t": 4},
                ],
            },
            {
                "isin": "GB00BMBL1G81",
                "name": "UKT 1.0% 2032",
                "coupon": 1.0,
                "maturity_date": "2032-01-31",
                "positions": [
                    {"type": "bond", "notional": 75_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -20_000_000, "counterparty": "Goldman Sachs", "repo_maturity_t": 1},
                    {"type": "repo", "notional": -15_000_000, "counterparty": "Morgan Stanley", "repo_maturity_t": 3},
                    {"type": "repo", "notional": -10_000_000, "counterparty": "HSBC", "repo_maturity_t": 5},
                ],
            },
            {
                "isin": "GB00BMV7TC07",
                "name": "UKT 4.25% 2034",
                "coupon": 4.25,
                "maturity_date": "2034-06-07",
                "positions": [
                    {"type": "bond", "notional": 100_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -30_000_000, "counterparty": "Citi", "repo_maturity_t": 3},
                ],
            },
            {
                "isin": "US30303M8T60",
                "name": "Meta 4.45% 2029",
                "coupon": 4.45,
                "maturity_date": "2029-08-15",
                "positions": [
                    {"type": "bond", "notional": 30_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -10_000_000, "counterparty": "Barclays", "repo_maturity_t": 1},
                    {"type": "repo", "notional": -5_000_000, "counterparty": "JPM", "repo_maturity_t": 2},
                ],
            },
        ],
    },
    {
        "id": "global-credit",
        "name": "Global Credit Opportunities",
        "bonds": [
            {
                "isin": "GB00BMV7TC07",
                "name": "UKT 4.25% 2034",
                "coupon": 4.25,
                "maturity_date": "2034-06-07",
                "positions": [
                    {"type": "bond", "notional": 60_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -25_000_000, "counterparty": "Deutsche Bank", "repo_maturity_t": 2},
                ],
            },
            {
                "isin": "US22890MAA09",
                "name": "CRWV 3.0% 2029",
                "coupon": 3.0,
                "maturity_date": "2029-02-15",
                "positions": [
                    {"type": "bond", "notional": 40_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -12_000_000, "counterparty": "Goldman Sachs", "repo_maturity_t": 1},
                    {"type": "repo", "notional": -8_000_000, "counterparty": "Barclays", "repo_maturity_t": 4},
                ],
            },
            {
                "isin": "GB00BNGJJN71",
                "name": "UKT 0.125% 2026",
                "coupon": 0.125,
                "maturity_date": "2026-01-30",
                "positions": [
                    {"type": "bond", "notional": 25_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -10_000_000, "counterparty": "Morgan Stanley", "repo_maturity_t": 3},
                ],
            },
            {
                "isin": "US30303M8T60",
                "name": "Meta 4.45% 2029",
                "coupon": 4.45,
                "maturity_date": "2029-08-15",
                "positions": [
                    {"type": "bond", "notional": 45_000_000, "counterparty": None, "repo_maturity_t": None},
                    {"type": "repo", "notional": -15_000_000, "counterparty": "JPM", "repo_maturity_t": 1},
                    {"type": "repo", "notional": -10_000_000, "counterparty": "Citi", "repo_maturity_t": 2},
                    {"type": "repo", "notional": -5_000_000, "counterparty": "HSBC", "repo_maturity_t": 5},
                ],
            },
        ],
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/portfolios")
def get_portfolios():
    return jsonify({"portfolios": PORTFOLIOS})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
