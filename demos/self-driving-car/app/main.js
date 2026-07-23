const carCanvas = document.getElementById("carCanvas");
const networkCanvas = document.getElementById("networkCanvas");
const stage = document.querySelector(".stage");

function layout() {
  const w = Math.min(stage.clientWidth || 900, 1100);
  const h = Math.min(window.innerHeight * 0.72, 720);
  const netW = Math.min(300, Math.floor(w * 0.32));
  const btnW = 52;
  carCanvas.width = Math.max(160, w - netW - btnW);
  carCanvas.height = h;
  networkCanvas.width = netW;
  networkCanvas.height = h;
}
layout();
window.addEventListener("resize", layout);

const carCtx = carCanvas.getContext("2d");
const networkCtx = networkCanvas.getContext("2d");

const road = new Road(carCanvas.width / 2, carCanvas.width * 0.9);

const N = 80;
const cars = generateCars(N);

let bestCar = cars[0];
const BRAIN_KEY = "ai-journey-self-driving-bestBrain";
if (localStorage.getItem(BRAIN_KEY)) {
  for (let i = 0; i < cars.length; i++) {
    cars[i].brain = JSON.parse(localStorage.getItem(BRAIN_KEY));
    if (i != 0) {
      NeuralNetwork.mutate(cars[i].brain, 0.1);
    }
  }
}

const traffic = [
  new Car(road.getLaneCenter(0), -100, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(1), -100, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(0), -300, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(2), -300, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(0), -500, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(1), -500, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(2), -700, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(2), -800, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(0), -1000, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(2), -1000, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(0), -1100, 30, 50, "DUMMY", 0, 2, getRandomColor()),
  new Car(road.getLaneCenter(2), -1100, 30, 50, "DUMMY", 0, 2, getRandomColor()),
];

const controlLabels = {
  forward: { color: "white", text: "↑" },
  left: { color: "white", text: "←" },
  right: { color: "white", text: "→" },
  reverse: { color: "white", text: "↓" },
};
generateImages(controlLabels);
const outputLabels = Object.values(controlLabels).map((s) => s.image);

animate();

function save() {
  localStorage.setItem(BRAIN_KEY, JSON.stringify(bestCar.brain));
}

function discard() {
  localStorage.removeItem(BRAIN_KEY);
}

function generateCars(n) {
  const list = [];
  for (let i = 1; i <= n; i++) {
    list.push(new Car(road.getLaneCenter(1), 100, 30, 50, "AI"));
  }
  return list;
}

function animate(time) {
  // keep road centered if canvas resized
  road.x = carCanvas.width / 2;
  road.width = carCanvas.width * 0.9;
  road.left = road.x - road.width / 2;
  road.right = road.x + road.width / 2;
  road.borders = [
    [
      { x: road.left, y: road.top },
      { x: road.left, y: road.bottom },
    ],
    [
      { x: road.right, y: road.top },
      { x: road.right, y: road.bottom },
    ],
  ];

  for (let i = 0; i < traffic.length; i++) {
    traffic[i].update(road.borders, []);
  }
  for (let i = 0; i < cars.length; i++) {
    cars[i].update(road.borders, traffic);
  }
  bestCar = cars.find((c) => c.y == Math.min(...cars.map((c) => c.y)));

  carCtx.clearRect(0, 0, carCanvas.width, carCanvas.height);
  carCtx.save();
  carCtx.translate(0, -bestCar.y + carCanvas.height * 0.7);

  road.draw(carCtx);
  for (let i = 0; i < traffic.length; i++) {
    traffic[i].draw(carCtx);
  }
  carCtx.globalAlpha = 0.2;
  for (let i = 0; i < cars.length; i++) {
    cars[i].draw(carCtx);
  }
  carCtx.globalAlpha = 1;
  bestCar.draw(carCtx, true);

  carCtx.restore();

  networkCtx.lineDashOffset = -time / 50;
  Visualizer.drawNetwork(networkCtx, bestCar.brain, outputLabels);
  requestAnimationFrame(animate);
}
