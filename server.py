from bird_app import app
port = int(os.environ.get("Port",5000))
app.run(debug=False, host='0.0.0.0', port=port)