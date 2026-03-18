from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Simple LOOK Algorithm
def scan(requests, head):
    requests = sorted(requests)
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    sequence = [head] + right + left[::-1]

    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement


def cscan(requests, head):
    requests = sorted(requests)
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    sequence = [head] + right + [max(requests)] + [min(requests)] + left

    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement


def look(requests, head):
    requests = sorted(requests)
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    sequence = [head] + right + left[::-1]

    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement


def clook(requests, head):
    requests = sorted(requests)
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    sequence = [head] + right + left

    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement
@app.route('/')
def home():
    return render_template("index.html");
@app.route('/run', methods=['POST'])
def run():
    data = request.json

    requests = list(map(int, data['requests'].split(',')))
    head = int(data['head'])
    algo = data['algorithm']

    if algo == "SCAN":
        sequence, movement = scan(requests, head)
    elif algo == "C-SCAN":
        sequence, movement = cscan(requests, head)
    elif algo == "LOOK":
        sequence, movement = look(requests, head)
    else:
        sequence, movement = clook(requests, head)

    # Calculate all for comparison
    scan_val = scan(requests, head)[1]
    cscan_val = cscan(requests, head)[1]
    look_val = look(requests, head)[1]
    clook_val = clook(requests, head)[1]

    # Graph
    plt.figure()
    plt.plot(sequence, marker='o')
    plt.xlabel("Step")
    plt.ylabel("Track")
    plt.title(algo + " Movement")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({
        "sequence": sequence,
        "movement": movement,
        "graph": graph_url,
        "scan": scan_val,
        "cscan": cscan_val,
        "look": look_val,
        "clook": clook_val
    })
    # Graph
    plt.figure()
    plt.plot(sequence, marker='o')
    plt.xlabel("Step")
    plt.ylabel("Floor")
    plt.title("Elevator Movement")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({
        "sequence": sequence,
        "movement": movement,
        "graph": graph_url
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)