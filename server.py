from flask import Flask
from bird_app import app


# app.run(debug=False)


if __name__ == '__main__':
# Bind to PORT if defined, otherwise default to 5000.
  import os
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)