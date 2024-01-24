from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def adventure_display():
    return render_template("index.html")

@app.route('/model1')
def model1():
    data1 = []
    data2 = []
    data3 = []

    with open('pick1.csv', 'r') as f1:
        reader1 = csv.reader(f1)
        data1 = [row for row in reader1]

    with open('pick2.csv', 'r') as f2:
        reader2 = csv.reader(f2)
        data2 = [row for row in reader2]

    with open('pick3.csv', 'r') as f3:
        reader3 = csv.reader(f3)
        data3 = [row for row in reader3]

    return render_template('model1.html', data1=data1, data2=data2, data3=data3)

@app.route('/model2')
def model2():
  data11 = []
  data22 = []
  data33 = []

  with open('GPT1.csv', 'r') as f1:
      reader1 = csv.reader(f1)
      data11 = [row for row in reader1]

  with open('GPT2.csv', 'r') as f2:
      reader2 = csv.reader(f2)
      data22 = [row for row in reader2]

  with open('GPT3.csv', 'r') as f3:
      reader3 = csv.reader(f3)
      data33 = [row for row in reader3]

  return render_template('model2.html', data1=data11, data2=data22, data3=data33)

@app.route('/model3')
def model3():

  return render_template('model3.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
