from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

dic = {'chair': '의자', 'sofa': '소파', 'table': '식탁', 'vacuum cleaner': '청소기'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image', methods = ['POST'])
def getimage():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename=="":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})

        try:
            file.save("./image/"+file.filename)
            val_path = "./image/" + file.filename
            result = subprocess.run("python ./yolov5/detect.py --weights ./yolov5/runs/train/gun_yolov5s_results/weights/best.pt --img 416 --conf 0.1 --source " + val_path, stdout=subprocess.PIPE, text=True)
            return jsonify({'name': dic[result.stdout.strip("\n")]})

        except:
            return jsonify({'error': 'error during prediction'})


if __name__ == '__main__':
    app.run(debug = True)