from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World! This is my Flask app running on Replit."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


##
##from flask import Flask, render_template, request
##
##app = Flask(__name__)
##
##@app.route('/')
##def home():
##    return render_template('index.html')  # You can add your HTML interface here
##
##@app.route('/run', methods=['POST'])
##def run_command():
##    # Run your command-line logic here
##    # For example:
##    result = "Hello from the command-line app!"
##    return render_template('index.html', result=result)
##
##if __name__ == '__main__':
##    app.run(host='0.0.0.0', port=8080)
