<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chronicle Vehicle Valuation System</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #08080a;
            --card-bg: #121216;
            --border-red: #3d0808;
            --accent-red: #8b0000;
            --bright-red: #dc143c;
            --text-light: #e0e0e0;
            --text-muted: #a0a0a0;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-dark);
            background: radial-gradient(circle at top, #1a0303 0%, #08080a 75%);
            color: var(--text-light);
            font-family: 'Montserrat', sans-serif;
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        h1 {
            font-family: 'Cinzel', serif;
            font-size: 2.8rem;
            color: var(--bright-red);
            letter-spacing: 4px;
            text-shadow: 0 0 15px rgba(220, 20, 60, 0.5);
            margin-bottom: 8px;
        }

        p.subtitle {
            font-family: 'Cinzel', serif;
            font-size: 1.1rem;
            color: var(--text-muted);
            letter-spacing: 2px;
        }

        .grid-layout {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-red);
            border-radius: 6px;
            padding: 25px;
            box-shadow: 0 5px 25px rgba(0, 0, 0, 0.8);
            transition: border-color 0.3s ease;
        }

        .card:hover {
            border-color: var(--bright-red);
        }

        .card-title {
            font-family: 'Cinzel', serif;
            font-size: 1.25rem;
            color: var(--bright-red);
            border-bottom: 1px solid var(--border-red);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        input, select {
            width: 100%;
            background-color: #0b0b0e;
            border: 1px solid #2a2a32;
            border-radius: 4px;
            padding: 10px 12px;
            color: #ffffff;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            border-color: var(--bright-red);
            box-shadow: 0 0 8px rgba(220, 20, 60, 0.4);
        }

        .btn-container {
            margin-top: 30px;
            text-align: center;
        }

        button {
            width: 100%;
            max-width: 400px;
            background: linear-gradient(180deg, #a00000 0%, #600000 100%);
            color: #ffffff;
            font-family: 'Cinzel', serif;
            font-size: 1.2rem;
            font-weight: 700;
            border: 1px solid var(--bright-red);
            border-radius: 4px;
            padding: 15px;
            cursor: pointer;
            letter-spacing: 2px;
            box-shadow: 0 0 15px rgba(139, 0, 0, 0.5);
            transition: all 0.3s ease;
        }

        button:hover {
            background: linear-gradient(180deg, #c00000 0%, #800000 100%);
            box-shadow: 0 0 25px rgba(220, 20, 60, 0.8);
        }

        .result-box {
            margin-top: 35px;
            background: #0f0303;
            border: 2px solid var(--bright-red);
            border-radius: 6px;
            padding: 30px;
            text-align: center;
            display: none;
            box-shadow: 0 0 30px rgba(139, 0, 0, 0.6);
        }

        .result-header {
            font-family: 'Cinzel', serif;
            font-size: 1.1rem;
            color: var(--text-muted);
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .result-price {
            font-family: 'Cinzel', serif;
            font-size: 3.2rem;
            font-weight: 900;
            color: #ff3333;
            text-shadow: 0 0 15px rgba(255, 51, 51, 0.6);
        }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>CHRONICLE VEHICLE VALUATION</h1>
        <p class="subtitle">AUTOMOTIVE MARKET PRICE ESTIMATION ENGINE</p>
    </header>

    <form id="valuation-form">
        <div class="grid-layout">
            <!-- Specification Inputs -->
            <div class="card">
                <div class="card-title">Specification</div>
                <div class="form-group">
                    <label>Make</label>
                    <input type="text" name="Make" value="Toyota" required>
                </div>
                <div class="form-group">
                    <label>Model</label>
                    <input type="text" name="Model" value="Camry" required>
                </div>
                <div class="form-group">
                    <label>Year</label>
                    <input type="number" name="Year" value="2020" min="1990" max="2026" required>
                </div>
                <div class="form-group">
                    <label>Body Type</label>
                    <select name="Body_Type">
                        <option value="Sedan">Sedan</option>
                        <option value="SUV">SUV</option>
                        <option value="Hatchback">Hatchback</option>
                        <option value="Coupe">Coupe</option>
                        <option value="Truck">Truck</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Color</label>
                    <select name="Color">
                        <option value="Black">Black</option>
                        <option value="White">White</option>
                        <option value="Silver">Silver</option>
                        <option value="Grey">Grey</option>
                        <option value="Red">Red</option>
                    </select>
                </div>
            </div>

            <!-- Performance Inputs -->
            <div class="card">
                <div class="card-title">Performance & Drive</div>
                <div class="form-group">
                    <label>Engine Size (L)</label>
                    <input type="number" step="0.1" name="Engine_Size" value="2.5" required>
                </div>
                <div class="form-group">
                    <label>Horsepower (HP)</label>
                    <input type="number" name="Horsepower" value="203" required>
                </div>
                <div class="form-group">
                    <label>Torque (Nm)</label>
                    <input type="number" name="Torque" value="250" required>
                </div>
                <div class="form-group">
                    <label>Transmission</label>
                    <select name="Transmission">
                        <option value="Automatic">Automatic</option>
                        <option value="Manual">Manual</option>
                        <option value="CVT">CVT</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Drivetrain</label>
                    <select name="Drivetrain">
                        <option value="FWD">FWD</option>
                        <option value="RWD">RWD</option>
                        <option value="AWD">AWD</option>
                        <option value="4WD">4WD</option>
                    </select>
                </div>
            </div>

            <!-- Usage & Condition Inputs -->
            <div class="card">
                <div class="card-title">Condition & History</div>
                <div class="form-group">
                    <label>Mileage (km)</label>
                    <input type="number" name="Mileage" value="45000" required>
                </div>
                <div class="form-group">
                    <label>Fuel Type</label>
                    <select name="Fuel_Type">
                        <option value="Petrol">Petrol</option>
                        <option value="Diesel">Diesel</option>
                        <option value="Hybrid">Hybrid</option>
                        <option value="Electric">Electric</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Fuel Efficiency (km/L)</label>
                    <input type="number" step="0.5" name="Fuel_Efficiency" value="15.0" required>
                </div>
                <div class="form-group">
                    <label>Owners</label>
                    <input type="number" name="Owners" value="1" min="0" max="10" required>
                </div>
                <div class="form-group">
                    <label>Accident History</label>
                    <select name="Accident_History">
                        <option value="None">None</option>
                        <option value="Minor">Minor</option>
                        <option value="Major">Major</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Service History</label>
                    <select name="Service_History">
                        <option value="Full Service History">Full Service History</option>
                        <option value="Partial Service History">Partial Service History</option>
                        <option value="No Record">No Record</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" name="Location" value="Urban" required>
                </div>
            </div>
        </div>

        <div class="btn-container">
            <button type="submit">CALCULATE ESTIMATED VALUE</button>
        </div>
    </form>

    <div class="result-box" id="result-box">
        <div class="result-header">ESTIMATED MARKET VALUE</div>
        <div class="result-price" id="result-price">$0.00</div>
    </div>
</div>

<script>
    document.getElementById('valuation-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            const resultBox = document.getElementById('result-box');
            const resultPrice = document.getElementById('result-price');

            if (result.success) {
                resultPrice.textContent = result.predicted_price;
                resultBox.style.display = 'block';
                resultBox.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert(result.error || 'Prediction error');
            }
        } catch (err) {
            alert('Failed to connect to valuation engine server.');
        }
    });
</script>

</body>
</html>
