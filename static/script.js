function runSimulation(){

    let requests = document.getElementById("requests").value;
    let head = document.getElementById("head").value;
    let algorithm = document.getElementById("algorithm").value;

    fetch('/run',{
        method:'POST',
        headers:{ 'Content-Type':'application/json' },
        body: JSON.stringify({
            requests: requests,
            head: head,
            algorithm: algorithm
        })
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("sequence").innerText =
            "Sequence: " + data.sequence.join(" → ");

        document.getElementById("movement").innerText =
            "Total Movement: " + data.movement;

        document.getElementById("graph").src =
            "data:image/png;base64," + data.graph;

        document.getElementById("scan").innerText = data.scan;
        document.getElementById("cscan").innerText = data.cscan;
        document.getElementById("look").innerText = data.look;
        document.getElementById("clook").innerText = data.clook;

        // MOVE ELEVATOR
        moveElevator(data.sequence);
    });
}
function moveElevator(sequence) {

    let elevator = document.getElementById("elevator");
    let i = 0;

    function move() {

        if (i >= sequence.length) return;

        let floor = parseInt(sequence[i]);

        let height = (floor - 1) * 40;

        height = Math.min(height, 440);
        height = Math.max(height, 0);

        elevator.style.bottom = height + "px";

        i++;
        setTimeout(move, 1000);
    }

    move();
}
function setScenario(event, type) {

    // Highlight active tab
    let buttons = document.querySelectorAll(".tabs button");
    buttons.forEach(btn => btn.classList.remove("active"));
    event.target.classList.add("active");

    let requests, head, algorithm;

    if (type === "app") {
        requests = "3,5,7,9,11";
        head = "2";
        algorithm = "SCAN";
    }
    else if (type === "file") {
        requests = "1,4,6,8,12";
        head = "3";
        algorithm = "LOOK";
    }
    else if (type === "db") {
        requests = "2,10,4,11,16";
        head = "5";
        algorithm = "C-SCAN";
    }

    // SET VALUES INTO INPUTS
    document.getElementById("requests").value = requests;
    document.getElementById("head").value = head;
    document.getElementById("algorithm").value = algorithm;

    // UPDATE QUEUE DISPLAY (IMPORTANT FIX)
    document.getElementById("queue").innerText = requests;

    // UPDATE ALGO NAME
    document.getElementById("algoName").innerText = algorithm;

    // 🔥 AUTO RUN SIMULATION (THIS WAS MISSING)
    runSimulation();
}
