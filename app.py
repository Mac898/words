from flask import Flask, render_template, request
import datetime
word_list = []

app = Flask(__name__)

def createList():
    print("Creating List...")
    out_string = ""
    for w in word_list:
        out_string = out_string + str(w) + ","
    print ("Saving File...")
    dt = datetime.datetime.now()
    time = datetime.datetime.timestamp(dt)
    f = open(str(time)+".txt", 'w+')
    f.write(out_string)
    f.close()
    print("File created: "+str(time)+".txt")
    return "File created: "+str(time)+".txt", out_string

@app.route('/', methods=['POST', 'GET'])
def index():
    global control_collectionopen
    global word_list
    if request.method == "POST":
        try:
            print("Collection: "+str(control_collectionopen))
            if control_collectionopen == False:
                return render_template('submit.html', complete_text='Submission Box Closed!')
            elif control_collectionopen == True:
                word = request.form['wts']
                print("Adding Word "+str(word))
                word_list.append(str(word))
                return render_template('submit.html', complete_text='Thanks, Submit another!')
        except NameError:
            return render_template('submit.html', complete_text='Not Initalized')
    else:
        return render_template('submit.html', complete_text="")

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    global control_collectionopen
    global word_list
    if request.method == "POST":
        if 'CloseCollection' in request.form:
            control_collectionopen = False
            print("Collection: "+str(control_collectionopen))
            return render_template('admin.html', complete_text="Closed Collection")
        if 'OpenCollection' in request.form:
            control_collectionopen = True
            print("Collection: "+str(control_collectionopen))
            return render_template('admin.html', complete_text="Opened Collection")
        if 'PrintList' in request.form:
            print("Print List")
            name, output = createList()
            return render_template('admin.html', complete_text="Printed List, "+name, printed_list=str(output))
        if 'ResetList' in request.form:
            print("Reset List")
            word_list.clear()
            return render_template('admin.html', complete_text="Reseted List")
    else:
        return render_template('admin.html', complete_text="")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')