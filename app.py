from flask import Flask, render_template
from flask_cors import CORS
from config import PORT
from routes.auth_routes import auth_bp
from routes.job_routes import jobs_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(jobs_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    import os
    # Exclude workspaces from file watcher
    extra_files = []
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)
