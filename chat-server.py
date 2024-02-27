from flask import Flask, send_from_directory, render_template, request, jsonify
import subprocess

app = Flask(__name__, static_folder='templates/static', template_folder='templates')

@app.route('/<path:path>')
def static_proxy(path):
    # Check if path is for a static file
    if path.startswith("static/"):
        # Correctly serve files from the static directory
        return send_from_directory('templates', path)
    else:
        # Serve other files like manifest.json, favicon.ico directly from the templates directory
        return send_from_directory('templates', path)

@app.route('/')
def serve():
    # Serve the main index.html file
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data['prompt']
    model = data['model']  # Receive the model from the request
    num_tokens = data.get('n', 4000)  # Default to 400 if not specified
    
    # Map model names to their respective commands
    model_commands = {
        'codellama-13b': "./main -m models/codellama-13b-instruct.Q2_K.gguf -p",
        'Model2': "./main -m models/model2.gguf -p",
        'Model3': "./main -m models/model3.gguf -p",
    }
    
    command_base = model_commands.get(model, model_commands['codellama-13b'])  # Fallback to Model1 if not found
    
    print(command_base)
    
    command = f'{command_base} "{prompt}" -n {num_tokens} -e'
    
    # Run your model as a subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Return the result
    return jsonify({"result": result.stdout})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
