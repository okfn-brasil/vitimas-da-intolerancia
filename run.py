from victims import app
from victims.settings import DEBUG, HOST, PORT


app.run(host=HOST, port=PORT, debug=DEBUG)
