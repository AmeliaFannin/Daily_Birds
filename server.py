from bird_app import app
port = int(os.environment.get("Port",5000))
app.run(debug=False, host='0.0.0.0', port=port)