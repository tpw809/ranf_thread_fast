"""Flask web app server for containerization and RESTFUL use.

Routes:

- bolted_joint_analysis: full analysis with all inputs
- material: process only a material input
- thread: process only a thread input
- fastener: process only a fastener (includes material and thread)
- nut_factor: process bolted joint up to estimating nut factor
- preload: process the joint only up to preload estimate (no external loads and no margins)
"""
from flask import Flask, request, jsonify

# import needed functionality:
# from thread_fast import Material
from thread_fast import process_material_input
#from thread_fast import ExternalMetricThread
#from thread_fast import InternalMetricThread
from thread_fast import process_metric_thread_input
# from thread_fast import Fastener
from thread_fast import process_fastener_input
# from thread_fast import BoltedJoint
from thread_fast import process_bolted_joint_input

app = Flask(__name__)
# app.secret_key='bunchofnumbersletters'


# @app.route('/black_box', methods=['POST'])
# def black_box():
#     print("starting thread_fast web app request...")
#     try:
#         # this should be a dictionary:
#         data = request.get_json()
#         print(data)
# 
#         # create object or call function or process input data:
#         black_box = BlackBox.from_json_data(data)
#         
#         # turn the crank:
#         black_box.turn_crank()
#         
#         # create result dictionary:
#         result = black_box.to_dict()
#         
#         print("... ending thread_fast web app request, returning json.")
#         return jsonify(result), 200
#     except KeyError:
#         return jsonify({'error': 'Invalid input. Send a proper input json object.'}), 400


@app.route('/bolted_joint_analysis', methods=['POST'])
def bolted_joint_analysis():
    try:
        # get posted json:
        data = request.get_json()
        print(f"\ninput data = \n{data}\n")
        
        # generate BoltedJoint object from input_dict:
        # obj = BoltedJoint.from_dict(input_dict=data)
        output_dict = process_bolted_joint_input(data)
        
        # return processed object dict:
        # return jsonify(obj.to_dict()), 200
        return jsonify(output_dict), 200
    except KeyError:
        print("KeyError")
        return jsonify({'error': 'Invalid input. Please provide a valid input JSON.'}), 400
    except AssertionError as e:
        print(f"AssertionError caught: {e}")
    except Exception as e:
        print(e)
    finally:
        pass


@app.route('/fastener', methods=['POST'])
def fastener():
    try:
        # get posted json:
        data = request.get_json()
        print(f"\ninput data = \n{data}\n")
        
        # generate Fastener object from input_dict:
        # obj = Material.from_dict(input_dict=data)
        output_dict = process_fastener_input(data)
        
        # return processed object dict:
        # return jsonify(obj.to_dict()), 200
        return jsonify(output_dict), 200
    except KeyError:
        return jsonify({'error': 'Invalid input. Please provide a valid input JSON.'}), 400


@app.route('/material', methods=['POST'])
def material():
    try:
        # get posted json:
        data = request.get_json()
        print(f"\ninput data = \n{data}\n")
        
        # generate Material from input_dict:
        # mat = Material.from_dict(input_dict=data)
        output_dict = process_material_input(input_dict=data)
        
        # return processed Material dict:
        # return jsonify(mat.to_dict()), 200
        return jsonify(output_dict), 200
    except KeyError:
        return jsonify({'error': 'Invalid input. Please provide a valid input JSON.'}), 400


@app.route('/thread', methods=['POST'])
def thread():
    try:
        # get posted json:
        data = request.get_json()
        print(f"\ninput data = \n{data}\n")
        
        # generate object from input_dict:
        # do I need to check what kind of thread is being used?
        
        # if data['type'] == 'ExternalMetricThread':
        #     obj = ExternalMetricThread.from_dict(input_dict=data)
        # elif data['type'] == 'InternalMetricThread':
        #     obj = InternalMetricThread.from_dict(input_dict=data)
        # else:
        #     raise Exception("no valid type.")
        
        # turn crank and return result dictionary:
        # result = obj.to_dict()
        result = process_metric_thread_input(data)
        
        return jsonify(result), 200
    except KeyError:
        return jsonify({'error': 'Invalid input. Please provide complete JSON input.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
