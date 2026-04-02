from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


# ---------------- VALIDATION ----------------
def get_float(data, key):
    value = data.get(key)

    if value is None:
        raise ValueError(f"{key} is required")

    try:
        return float(value)
    except:
        raise ValueError(f"{key} must be a number")


# ---------------- BASIC CALCULATIONS ----------------
def calc_transmit(p_single, n):
    if n <= 0:
        raise ValueError("n must be greater than 0")

    return round(p_single + 10 * math.log10(n), 2)


def calc_downstream(p_pre, p_pre_single, p_single_in):
    return round(p_pre - (p_pre_single - p_single_in), 2)


def calc_second(p_first, p_first_single, p_second_single, offset):
    return round(p_first - (p_first_single - p_second_single) + offset, 2)


# ---------------- MIXED LAMBDA CALC ----------------
def dbm_to_mw(dbm):
    return 10 ** (dbm / 10)


def mw_to_dbm(mw):
    if mw <= 0:
        raise ValueError("Power must be greater than 0")
    return 10 * math.log10(mw)


def calc_mixed_power_3(p1_a, n_a, p1_b, n_b, p1_c, n_c):
    # Step 1: calculate total dBm per group
    p_a = calc_transmit(p1_a, n_a)
    p_b = calc_transmit(p1_b, n_b)
    p_c = calc_transmit(p1_c, n_c)

    # Step 2: convert to mW
    mw_a = dbm_to_mw(p_a)
    mw_b = dbm_to_mw(p_b)
    mw_c = dbm_to_mw(p_c)

    # Step 3: sum all
    total_mw = mw_a + mw_b + mw_c

    # Step 4: convert back to dBm
    total_dbm = round(mw_to_dbm(total_mw), 2)

    return {
        "p_a": p_a,
        "p_b": p_b,
        "p_c": p_c,
        "total": total_dbm
    }


# ---------------- ERROR HANDLER ----------------
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate/transmit", methods=["POST"])
def transmit():
    data = request.json or {}

    p_single = get_float(data, "p_single")
    n = int(get_float(data, "n"))

    result = calc_transmit(p_single, n)
    return jsonify({"result": result})


@app.route("/calculate/downstream", methods=["POST"])
def downstream():
    data = request.json or {}

    p_pre = get_float(data, "p_pre")
    p_pre_single = get_float(data, "p_pre_single")
    p_single_in = get_float(data, "p_single_in")

    result = calc_downstream(p_pre, p_pre_single, p_single_in)
    return jsonify({"result": result})


@app.route("/calculate/second", methods=["POST"])
def second():
    data = request.json or {}

    p_first = get_float(data, "p_first")
    p_first_single = get_float(data, "p_first_single")
    p_second_single = get_float(data, "p_second_single")
    offset = get_float(data, "offset")

    result = calc_second(p_first, p_first_single, p_second_single, offset)
    return jsonify({"result": result})


@app.route("/calculate/mixed", methods=["POST"])
def mixed():
    data = request.json or {}

    p1_a = get_float(data, "p1_a")
    n_a = get_float(data, "n_a")

    p1_b = get_float(data, "p1_b")
    n_b = get_float(data, "n_b")

    p1_c = get_float(data, "p1_c")
    n_c = get_float(data, "n_c")

    result = calc_mixed_power_3(p1_a, n_a, p1_b, n_b, p1_c, n_c)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)