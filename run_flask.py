
from flask import Flask
from flask import request
import lisp

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def root():
    if request.method=='GET':
        return 'Method GET'
    elif request.method=='POST':
        command = request.get_data().decode('utf8')
        result, error = lisp.execute_request(command)
        if not error:
            return result
        return result,500


# -----------------------------------


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)



