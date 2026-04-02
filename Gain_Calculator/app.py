from flask import Flask, request, jsonify, render_template
import math

# ================= INIT =================
app = Flask(__name__)

# ================= CORE =================
def dbm_to_mw(dbm):
    return 10 ** (dbm / 10)

def mw_to_dbm(mw):
    if mw <= 0:
        return -100
    return 10 * math.log10(mw)

def total_dbm(values):
    return mw_to_dbm(sum(dbm_to_mw(v) for v in values))


# ================= MODULE DATA =================
MODULES_96 = {
    "101": [
        {"gain": 20, "pin_range": (-20.3, -18.3), "pout_nom": 1.7},
        {"gain": 26, "pin_range": (-26.3, -24.3), "pout_nom": 1.7},
        {"gain": 31, "pin_range": (-32, -29.3),  "pout_nom": 1.7}
    ],
    "105": [
        {"gain": 23, "pin_range": (-21, -19), "pout_nom": 4},
        {"gain": 29, "pin_range": (-27, -25), "pout_nom": 4},
        {"gain": 32, "pin_range": (-32, -28), "pout_nom": 4}
    ],
    "106": [
        {"gain": 13, "pin_range": (-13.3, -11.3), "pout_nom": 1.7},
        {"gain": 18, "pin_range": (-18.3, -16.3), "pout_nom": 1.7},
        {"gain": 23, "pin_range": (-24, -21.3),  "pout_nom": 1.7}
    ],
    "107": [
        {"gain": 17, "pin_range": (-15, -13), "pout_nom": 4},
        {"gain": 21, "pin_range": (-19, -17), "pout_nom": 4},
        {"gain": 25, "pin_range": (-24, -21), "pout_nom": 4}
    ]
}


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/single_amp", methods=["POST"])
def single_amp():
    data = request.json

    # ===== INPUT =====
    tx_module = data.get("module")
    rx_module = data.get("rx_module")
    pin = data.get("pin", [])
    pout = data.get("pout", [])
    span_loss = float(data.get("span_loss", 0))

    # ===== VALIDATION =====
    if not tx_module or tx_module not in MODULES_96:
        return jsonify({"error": "Invalid TX module"}), 400

    if not rx_module or rx_module not in MODULES_96:
        return jsonify({"error": "Invalid RX module"}), 400

    if not pin or not pout or len(pin) != len(pout):
        return jsonify({"error": "Invalid input/output"}), 400

    # ================= TX =================
    pin_total = total_dbm(pin)
    pout_total = total_dbm(pout)
    tx_gain = round(pout_total - pin_total, 2)

    pin_avg = sum(pin) / len(pin)

    tx_selected = None
    for p in MODULES_96[tx_module]:
        low, high = p["pin_range"]
        if low <= pin_avg <= high:
            tx_selected = p
            break

    if not tx_selected:
        tx_selected = min(
            MODULES_96[tx_module],
            key=lambda x: abs(pin_avg - ((x["pin_range"][0] + x["pin_range"][1]) / 2))
        )

    tx_expected_gain = tx_selected["gain"]
    tx_gain_diff = round(tx_gain - tx_expected_gain, 2)
    tx_status = "OK" if abs(tx_gain_diff) <= 2 else "MISMATCH"

    # ================= FIBER + RX =================
    p_rx_in = round(pout_total - span_loss, 2)
    rx_gain = round(pout_total - p_rx_in, 2)

    # RX profile selection (based on RX input)
    rx_selected = None
    for p in MODULES_96[rx_module]:
        low, high = p["pin_range"]
        if low <= p_rx_in <= high:
            rx_selected = p
            break

    if not rx_selected:
        rx_selected = min(
            MODULES_96[rx_module],
            key=lambda x: abs(p_rx_in - ((x["pin_range"][0] + x["pin_range"][1]) / 2))
        )

    rx_expected_gain = rx_selected["gain"]
    rx_gain_diff = round(rx_gain - rx_expected_gain, 2)
    rx_status = "OK" if abs(rx_gain_diff) <= 2 else "MISMATCH"

    # ================= ANALYSIS =================
    pout_nom = tx_selected["pout_nom"]
    deviations = [round(p - pout_nom, 2) for p in pout]

    tilt = round(max(pin) - min(pin), 2)
    tilt_status = "OK" if tilt <= 2 else "MODERATE" if tilt <= 5 else "HIGH"

    # ================= RESPONSE =================
    return jsonify({
        "channels": len(pin),

        # TX
        "tx_module": tx_module,
        "pin_total": round(pin_total, 2),
        "pout_total": round(pout_total, 2),
        "tx_gain": tx_gain,
        "tx_profile": tx_expected_gain,
        "tx_gain_diff": tx_gain_diff,
        "tx_status": tx_status,

        # FIBER + RX
        "span_loss": span_loss,
        "p_rx_in": p_rx_in,
        "rx_gain": rx_gain,
        "rx_module": rx_module,
        "rx_profile": rx_expected_gain,
        "rx_gain_diff": rx_gain_diff,
        "rx_status": rx_status,

        # ANALYSIS
        "tilt": tilt,
        "tilt_status": tilt_status,
        "deviations": deviations
    })


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)