from flask import Flask, request, abort
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure the logger
log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] - %(message)s"
)
log_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=1024 * 1024,  # 1 MB per log file
    backupCount=3,  # Keep 3 backup log files
)
log_handler.setFormatter(log_formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(log_handler)

@app.route('/', methods = ['GET', 'POST', 'PUT'])
def index():
    client_ip = request.remote_addr
    
    if request.method != 'GET':
        request_type=request.method
        app.logger.warning(f"Unauthorized {request_type} at the index page - IP: {client_ip}")

    app.logger.info(f"Accessed the index page - IP:{client_ip}")
    return "Hello, World!"

@app.route('/operation', methods=['GET', 'POST', 'PUT'])
def operation():
    if request.method == "GET":
        client_ip = request.remote_addr
        app.logger.info(f"GET request on operation page - IP:{client_ip}")
        return "Other Page sucessful GET request"
    elif request.method == "POST":
        client_ip = request.remote_addr
        app.logger.info(f"POST request on operation page - IP:{client_ip}")
        return "Other Page Successful POST request"
    else:
        client_ip = request.remote_addr
        app.logger.error(f"Unauthorized {request.method} on the operation page - IP:{client_ip}")
        abort(403)

if __name__ == '__main__':
    app.run(debug=True)
