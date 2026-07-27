import os
import joblib
import pandas as pd
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# 1. Automatic Static CSS Creation
# ---------------------------------------------------------------------------
os.makedirs('static', exist_ok=True)
CSS_PATH = os.path.join('static', 'style.css')

CSS_CONTENT = """
:root {
    --bg-dark: #0a0a0c;
    --card-bg: rgba(18, 18, 22, 0.85);
    --border-color: #2a2a32;
    --accent-red: #8b0000;
    --glow-red: #ff1e27;
    --text-primary: #e0e0e8;
    --text-muted: #8a8a9a;
    --font-heading: 'Cinzel', serif;
    --font-body: 'Inter', sans-serif;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background-color: var(--bg-dark);
    color: var(--text-primary);
    font-family: var(--font-body);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    padding: 2rem 1rem;
    overflow-x: hidden;
}

.background-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: 
        radial-gradient(circle at 50% 10%, rgba(139, 0, 0, 0.15), transparent 60%),
        radial-gradient(circle at 80% 80%, rgba(20, 20, 25, 0.8), transparent 50%);
    z-index: -1;
}

.container {
    width: 100%;
    max-width: 900px;
}

.header {
    text-align: center;
    margin-bottom: 2rem;
}

.title {
    font-family: var(--font-heading);
    font-size: 2.5rem;
    letter-spacing: 4px;
    color: #ffffff;
    text-shadow: 0 0 10px rgba(255, 30, 39, 0.5);
    margin-bottom: 0.5rem;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    letter-spacing: 1px;
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 15px rgba(139, 0, 0, 0.2);
    border-radius: 4px;
    padding: 2.5rem;
    backdrop-filter: blur(8px);
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.25rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

label {
    font-family: var(--font-heading);
    font-size: 0.8rem;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
    text-transform: uppercase;
}

input, select {
    background: #121216;
    border: 1px solid var(--border-color);
    color: #ffffff;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    border-radius: 2px;
    outline: none;
    transition: all 0.3s ease;
}

input:focus, select:focus {
    border-color: var(--accent-red);
    box-shadow: 0 0 8px rgba(255, 30, 39, 0.4);
}

.action-container {
    margin-top: 2rem;
    text-align: center;
}

.btn {
    background: linear-gradient(135deg, #4a0000, var(--accent-red));
    color: #ffffff;
    font-family: var(--font-heading);
    font-size: 1rem;
    letter-spacing: 2px;
    border: 1px solid var(--accent-red);
    padding: 0.9rem 2.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    max-width: 320px;
}

.btn:hover {
    background: linear-gradient(135deg, var(--accent-red), var(--glow-red));
    box-shadow: 0 0 15px rgba(255, 30, 39, 0.6);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.result-box {
    margin-top: 2rem;
    padding: 1.5rem;
    background: rgba(139, 0, 0, 0.15);
    border: 1px solid var(--accent-red);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    animation: fadeIn 0.4s ease;
}

.result-label {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    letter-spacing: 2px;
    color: var(--text-muted);
}

.result-value {
    font-family: var(--font-heading);
    font-size: 2.2rem;
    color: #ffffff;
    text-shadow: 0 0 10px var(--glow-red);
}

.error-box {
    margin-top: 1.5rem;
    padding: 1rem;
    background: rgba(255, 30, 39, 0.1);
    border: 1px solid var(--glow-red);
    color: var(--glow-red);
    text-align: center;
    font-size: 0.9rem;
}

.hidden {
    display: none;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
"""

with open(CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(CSS_CONTENT)

# ---------------------------------------------------------------------------
# 2. Embedded HTML Template
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valuation Ledger | Automated Price Estimation</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="background-overlay"></div>
    <main class="container">
        <header class="header">
            <h1 class="title">THE VALUATION LEDGER</h1>
            <p class="subtitle">Enter the specifications to calculate the ultimate market value.</p>
        </header>

        <section class="card">
            <form id="valuationForm">
                <div class="grid">
                    <div class="form-group">
                        <label for="Make">Make</label>
                        <input type="text" id="Make" name="Make" placeholder="e.g. Toyota" required>
                    </div>

                    <div class="form-group">
                        <label for="Model">Model</label>
                        <input type="text" id="Model" name="Model" placeholder="e.g. Corolla" required>
                    </div>

                    <div class="form-group">
                        <label for="Year">Year</label>
                        <input type="number" id="Year" name="Year" min="1900" max="2027" placeholder="e.g. 2020" required>
                    </div>

                    <div class="form-group">
                        <label for="Engine_Size">Engine Size (L)</label>
                        <input type="number" step="0.1" id="Engine_Size" name="Engine_Size" placeholder="e.g. 2.0" required>
                    </div>

                    <div class="form-group">
                        <label for="Mileage">Mileage (Miles)</label>
                        <input type="number" id="Mileage" name="Mileage" placeholder="e.g. 45000" required>
                    </div>

                    <div class="form-group">
                        <label for="Horsepower">Horsepower</label>
                        <input type="number" id="Horsepower" name="Horsepower" placeholder="e.g. 180" required>
                    </div>

                    <div class="form-group">
                        <label for="Torque">Torque (lb-ft)</label>
                        <input type="number" id="Torque" name="Torque" placeholder="e.g. 200" required>
                    </div>

                    <div class="form-group">
                        <label for="Fuel_Efficiency">Fuel Efficiency (MPG)</label>
                        <input type="number" step="0.1" id="Fuel_Efficiency" name="Fuel_Efficiency" placeholder="e.g. 30" required>
                    </div>

                    <div class="form-group">
                        <label for="Fuel_Type">Fuel Type</label>
                        <select id="Fuel_Type" name="Fuel_Type" required>
                            <option value="" disabled selected>Select Fuel Type</option>
                            <option value="Gasoline">Gasoline</option>
                            <option value="Diesel">Diesel</option>
                            <option value="Electric">Electric</option>
                            <option value="Hybrid">Hybrid</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="Transmission">Transmission</label>
                        <select id="Transmission" name="Transmission" required>
                            <option value="" disabled selected>Select Transmission</option>
                            <option value="Automatic">Automatic</option>
                            <option value="Manual">Manual</option>
                            <option value="CVT">CVT</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="Drivetrain">Drivetrain</label>
                        <select id="Drivetrain" name="Drivetrain" required>
                            <option value="" disabled selected>Select Drivetrain</option>
                            <option value="FWD">FWD</option>
                            <option value="RWD">RWD</option>
                            <option value="AWD">AWD</option>
                            <option value="4WD">4WD</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="Body_Type">Body Type</label>
                        <input type="text" id="Body_Type" name="Body_Type" placeholder="e.g. Sedan, SUV" required>
                    </div>

                    <div class="form-group">
                        <label for="Owners">Previous Owners</label>
                        <input type="number" id="Owners" name="Owners" min="0" placeholder="e.g. 1" required>
                    </div>

                    <div class="form-group">
                        <label for="Accident_History">Accident History</label>
                        <select id="Accident_History" name="Accident_History" required>
                            <option value="" disabled selected>Select History</option>
                            <option value="None">None</option>
                            <option value="Minor">Minor</option>
                            <option value="Major">Major</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="Service_History">Service History</label>
                        <select id="Service_History" name="Service_History" required>
                            <option value="" disabled selected>Select Service Record</option>
                            <option value="Full">Full / Regular</option>
                            <option value="Partial">Partial</option>
                            <option value="None">None</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="Color">Color</label>
                        <input type="text" id="Color" name="Color" placeholder="e.g. Black" required>
                    </div>

                    <div class="form-group full-width">
                        <label for="Location">Location</label>
                        <input type="text" id="Location" name="Location" placeholder="e.g. New York, NY" required>
                    </div>
                </div>

                <div class="action-container">
                    <button type="submit" id="submitBtn" class="btn">EXECUTE ESTIMATION</button>
                </div>
            </form>

            <div id="resultModal" class="result-box hidden">
                <span class="result-label">ESTIMATED VALUATION</span>
                <span id="predictedPrice" class="result-value">$0.00</span>
            </div>

            <div id="errorMessage" class="error-box hidden"></div>
        </section>
    </main>

    <script>
        document.getElementById('valuationForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = document.getElementById('submitBtn');
            const resultModal = document.getElementById('resultModal');
            const errorMessage = document.getElementById('errorMessage');
            const predictedPrice = document.getElementById('predictedPrice');

            submitBtn.disabled = true;
            submitBtn.innerText = "CALCULATING...";
            resultModal.classList.add('hidden');
            errorMessage.classList.add('hidden');

            const formData = new FormData(e.target);
            const payload = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    predictedPrice.innerText = data.predicted_price;
                    resultModal.classList.remove('hidden');
                } else {
                    errorMessage.innerText = data.error || "An unknown error occurred.";
                    errorMessage.classList.remove('hidden');
                }
            } catch (err) {
                errorMessage.innerText = "Network failure or server unavailable.";
                errorMessage.classList.remove('hidden');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = "EXECUTE ESTIMATION";
            }
        });
    </script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# 3. Model Loading & Flask Backend Logic
# ---------------------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'V_Price_estimater_RFR.pkl')

FEATURE_NAMES = [
    'Make', 'Model', 'Year', 'Fuel_Type', 'Transmission',
    'Engine_Size', 'Mileage', 'Horsepower', 'Torque',
    'Owners', 'Accident_History', 'Service_History',
    'Color', 'Body_Type', 'Drivetrain', 'Fuel_Efficiency', 'Location'
]

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model file not loaded.'}), 500

    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        input_data = {}
        for feature in FEATURE_NAMES:
            val = data.get(feature)
            if val is None or val == '':
                return jsonify({'error': f'Missing value for feature: {feature}'}), 400
            
            try:
                input_data[feature] = [float(val)]
            except ValueError:
                input_data[feature] = [val]

        input_df = pd.DataFrame(input_data)
        prediction = model.predict(input_df)[0]
        formatted_price = f"${prediction:,.2f}"

        return jsonify({'success': True, 'predicted_price': formatted_price})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
