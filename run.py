from violence import app
from violence.settings import DEBUG, HOST, PORT


app.run(host=HOST, port=PORT, debug=DEBUG)
