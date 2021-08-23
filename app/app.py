from flask import Flask, render_template, request
import numpy as np
from joblib import load
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)


@app.route('/')
def hello_world():
    test_np_input = np.array([[1], [2], [17]])
    model = load('model.joblib')
    preds = model.predict(test_np_input)
    preds_as_str = str(preds)
    return preds_as_str



def make_picture(training_data_filename, model, new_inp_np_arr, output_file):
  data = pd.read_pickle(training_data_filename)
  ages = data['Age']
  data = data[ages > 0]
  ages = data['Age']
  heights = data['Height']
  x_new = np.array(list(range(19))).reshape(19, 1)
  preds = model.predict(x_new)

  fig = px.scatter(x=ages, y=heights, title="Height vs Age of People", labels={'x': 'Age (years)',
                                                                                'y': 'Height (inches)'})

  fig.add_trace(go.Scatter(x=x_new.reshape(19), y=preds, mode='lines', name='Model'))

  new_preds = model.predict(new_inp_np_arr)

  fig.add_trace(go.Scatter(x=new_inp_np_arr.reshape(len(new_inp_np_arr)), y=new_preds, name='New Outputs', mode='markers', marker=dict(color='purple', size=20, line=dict(color='purple', width=2))))
  
  fig.write_image(output_file, width=800, engine='kaleido')
  fig.show()

def floats_string_to_np_arr(floats_str):
  def is_float(s):
    try:
      float(s)
      return True
    except:
      return False
  floats = np.array([float(x) for x in floats_str.split(',') if is_float(x)])
  return floats.reshape(len(floats), 1)