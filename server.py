import os
from flask import Flask
from bird_app import app


app.run(debug=False)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
# Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 33507))
  app.run(host='0.0.0.0', port=port)