<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SNAKE — Dot Matrix</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;500;600&display=swap');

  :root{
    --case: #33353a;
    --case-hi: #45484f;
    --case-lo: #222327;
    --screen-bg: #c7d6a0;
    --screen-bg-lit: #d3e0ae;
    --dot-off: #b7c691;
    --dot-on: #34401c;
    --dot-head: #232c12;
    --dot-food: #7a2f2f;
    --silver: #9a9ea6;
    --ivory: #e7e7e5;
    --muted: #8b8d92;
  }

  *{ box-sizing: border-box; }

  html, body{
    margin:0;
    min-height: 100vh;
    background:
      radial-gradient(ellipse at 50% 0%, #1c1d20 0%, #0e0e10 70%);
    color: var(--ivory);
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  body{
    display:flex;
    flex-direction: column;
    align-items:center;
    justify-content:center;
    padding: 40px 16px;
    gap: 22px;
  }

  .eyebrow{
    display:flex;
    align-items:center;
    gap:10px;
    font-size: 10px;
    letter-spacing: 0.24em;
    text-transform:uppercase;
    color: var(--muted);
    font-weight:600;
  }
  .eyebrow::before, .eyebrow::after{
    content:"";
    width:14px;
    height:1px;
    background: var(--muted);
  }

  /* ---- Handheld case ---- */
  .device{
    width: 340px;
    max-width: 92vw;
    background: linear-gradient(160deg, var(--case-hi), var(--case) 40%, var(--case-lo) 100%);
    border-radius: 34px;
    padding: 20px 20px 26px;
    box-shadow:
      0 40px 70px -25px rgba(0,0,0,0.65),
      inset 0 1px 0 rgba(255,255,255,0.08),
      inset 0 -2px 0 rgba(0,0,0,0.35);
    border: 1px solid #17181a;
  }

  .speaker{
    display:flex;
    justify-content:center;
    gap: 6px;
    margin-bottom: 14px;
  }
  .speaker span{
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--case-lo);
    box-shadow: inset 0 1px 1px rgba(0,0,0,0.6);
  }

  .brand{
    text-align:center;
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    letter-spacing: 0.08em;
    color: var(--silver);
    margin-bottom: 12px;
  }

  /* ---- LCD screen ---- */
  .screen{
    background: linear-gradient(175deg, var(--screen-bg-lit), var(--screen-bg));
    border-radius: 6px;
    padding: 10px;
    box-shadow:
      inset 0 3px 10px rgba(0,0,0,0.35),
      inset 0 0 0 2px #8d9a6c,
      inset 0 0 0 4px #6d7952;
    position: relative;
  }

  .hud{
    display:flex;
    justify-content:space-between;
    align-items:baseline;
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--dot-on);
    padding: 2px 4px 8px;
    letter-spacing: 0.02em;
  }

  canvas{
    display:block;
    width: 100%;
    height: auto;
    image-rendering: pixelated;
    border-radius: 2px;
  }

  .overlay{
    position:absolute;
    inset: 10px;
    top: 46px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    background: rgba(199, 214, 160, 0.94);
    border-radius: 4px;
    padding: 16px;
    gap: 10px;
  }
  .overlay.hidden{ display:none; }
  .overlay h2{
    font-family: 'Press Start 2P', monospace;
    font-size: 13px;
    color: var(--dot-on);
    margin: 0;
    line-height: 1.6;
  }
  .overlay p{
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #4a5730;
    margin: 0;
    line-height: 1.8;
  }
  .overlay button{
    margin-top: 4px;
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    background: var(--dot-on);
    color: var(--screen-bg);
    border: none;
    padding: 10px 18px;
    border-radius: 3px;
    cursor: pointer;
  }
  .overlay button:active{ transform: translateY(1px); }

  /* ---- D-pad ---- */
  .controls{
    display:flex;
    justify-content: space-between;
    align-items:center;
    margin-top: 22px;
    padding: 0 6px;
  }

  .dpad{
    display: grid;
    grid-template-columns: 40px 40px 40px;
    grid-template-rows: 40px 40px 40px;
    gap: 3px;
  }
  .dpad button{
    background: linear-gradient(160deg, #4a4d54, #2a2c30);
    border: 1px solid #1a1b1d;
    border-radius: 8px;
    color: var(--silver);
    font-size: 15px;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    box-shadow: 0 3px 0 #17181a, inset 0 1px 0 rgba(255,255,255,0.08);
    -webkit-tap-highlight-color: transparent;
  }
  .dpad button:active{
    transform: translateY(2px);
    box-shadow: 0 1px 0 #17181a, inset 0 1px 0 rgba(255,255,255,0.08);
  }
  .dpad .up{ grid-column:2; grid-row:1; }
  .dpad .left{ grid-column:1; grid-row:2; }
  .dpad .center{ grid-column:2; grid-row:2; background: var(--case-lo); }
  .dpad .right{ grid-column:3; grid-row:2; }
  .dpad .down{ grid-column:2; grid-row:3; }

  .side-info{
    display:flex;
    flex-direction:column;
    align-items:flex-end;
    gap: 8px;
    font-size: 10px;
    color: var(--muted);
    line-height: 1.6;
    text-align:right;
  }
  .side-info kbd{
    background: var(--case-lo);
    border: 1px solid #17181a;
    border-radius: 3px;
    padding: 1px 5px;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: var(--silver);
  }

  .hint{
    font-size: 11px;
    color: var(--muted);
    text-align:center;
    max-width: 320px;
  }

  @media (prefers-reduced-motion: reduce){
    * { transition: none !important; animation: none !important; }
  }
</style>
</head>
<body>

<div class="eyebrow">Classic handheld</div>

<div class="device">
  <div class="speaker">
    <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
  </div>
  <div class="brand">SNAKE · DOT MATRIX</div>

  <div class="screen">
    <div class="hud">
      <span id="scoreLabel">SCORE 000</span>
      <span id="highLabel">HI 000</span>
    </div>
    <canvas id="game" width="220" height="220"></canvas>
    <div class="overlay" id="overlay">
      <h2>SNAKE</h2>
      <p>ARROWS / WASD<br>OR THE PAD BELOW</p>
      <button id="startBtn">START</button>
    </div>
  </div>

  <div class="controls">
    <div class="dpad">
      <button class="up" data-dir="up" aria-label="Up">▲</button>
      <button class="left" data-dir="left" aria-label="Left">◀</button>
      <div class="center"></div>
      <button class="right" data-dir="right" aria-label="Right">▶</button>
      <button class="down" data-dir="down" aria-label="Down">▼</button>
    </div>
    <div class="side-info">
      <span><kbd>W A S D</kbd></span>
      <span>or arrow keys</span>
      <span><kbd>SPACE</kbd> to restart</span>
    </div>
  </div>
</div>

<p class="hint">Eat the food to grow. The screen doesn't wrap — hitting the edge or your own tail ends the run.</p>

<script>
  const COLS = 20, ROWS = 20;
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  const cell = canvas.width / COLS;

  const scoreLabel = document.getElementById('scoreLabel');
  const highLabel = document.getElementById('highLabel');
  const overlay = document.getElementById('overlay');
  const startBtn = document.getElementById('startBtn');

  let snake, dir, pendingDir, food, score, highScore, tickMs, loopHandle, running;
  highScore = 0;

  function resetState(){
    snake = [
      {x: 10, y: 10},
      {x: 9, y: 10},
      {x: 8, y: 10}
    ];
    dir = 'right';
    pendingDir = 'right';
    score = 0;
    tickMs = 150;
    placeFood();
    updateHud();
  }

  function placeFood(){
    let candidate;
    do {
      candidate = { x: Math.floor(Math.random()*COLS), y: Math.floor(Math.random()*ROWS) };
    } while (snake.some(s => s.x === candidate.x && s.y === candidate.y));
    food = candidate;
  }

  function updateHud(){
    scoreLabel.textContent = 'SCORE ' + String(score).padStart(3, '0');
    highLabel.textContent = 'HI ' + String(highScore).padStart(3, '0');
  }

  function roundDot(px, py, size, r){
    ctx.beginPath();
    ctx.moveTo(px + r, py);
    ctx.arcTo(px + size, py, px + size, py + size, r);
    ctx.arcTo(px + size, py + size, px, py + size, r);
    ctx.arcTo(px, py + size, px, py, r);
    ctx.arcTo(px, py, px + size, py, r);
    ctx.closePath();
    ctx.fill();
  }

  function draw(){
    // Base unlit LCD dot grid
    for (let r = 0; r < ROWS; r++){
      for (let c = 0; c < COLS; c++){
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--dot-off');
        roundDot(c*cell + 1, r*cell + 1, cell - 2, 2);
      }
    }

    // Food
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--dot-food');
    roundDot(food.x*cell + 1, food.y*cell + 1, cell - 2, 3);

    // Snake body
    snake.forEach((seg, i) => {
      ctx.fillStyle = i === 0
        ? getComputedStyle(document.documentElement).getPropertyValue('--dot-head')
        : getComputedStyle(document.documentElement).getPropertyValue('--dot-on');
      roundDot(seg.x*cell + 1, seg.y*cell + 1, cell - 2, 2);
    });
  }

  function tick(){
    dir = pendingDir;
    const head = { ...snake[0] };
    if (dir === 'up') head.y -= 1;
    if (dir === 'down') head.y += 1;
    if (dir === 'left') head.x -= 1;
    if (dir === 'right') head.x += 1;

    // Wall collision
    if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS){
      return gameOver();
    }
    // Self collision
    if (snake.some(s => s.x === head.x && s.y === head.y)){
      return gameOver();
    }

    snake.unshift(head);

    if (head.x === food.x && head.y === food.y){
      score += 10;
      if (score > highScore) highScore = score;
      tickMs = Math.max(70, tickMs - 3);
      placeFood();
      updateHud();
      restartLoop();
    } else {
      snake.pop();
    }

    draw();
  }

  function restartLoop(){
    clearInterval(loopHandle);
    loopHandle = setInterval(tick, tickMs);
  }

  function gameOver(){
    running = false;
    clearInterval(loopHandle);
    overlay.classList.remove('hidden');
    overlay.querySelector('h2').textContent = 'GAME OVER';
    overlay.querySelector('p').innerHTML = 'SCORE ' + String(score).padStart(3,'0') + '<br>TRY AGAIN?';
    startBtn.textContent = 'RESTART';
  }

  function startGame(){
    resetState();
    running = true;
    overlay.classList.add('hidden');
    draw();
    restartLoop();
  }

  function setDirection(next){
    if (!running) return;
    const opposite = { up:'down', down:'up', left:'right', right:'left' };
    if (opposite[next] === dir) return;
    pendingDir = next;
  }

  // Keyboard controls
  window.addEventListener('keydown', (e) => {
    const map = {
      ArrowUp:'up', ArrowDown:'down', ArrowLeft:'left', ArrowRight:'right',
      w:'up', s:'down', a:'left', d:'right',
      W:'up', S:'down', A:'left', D:'right'
    };
    if (map[e.key]){
      e.preventDefault();
      setDirection(map[e.key]);
    }
    if (e.key === ' '){
      e.preventDefault();
      startGame();
    }
  });

  // D-pad controls
  document.querySelectorAll('.dpad button[data-dir]').forEach(btn => {
    btn.addEventListener('click', () => setDirection(btn.dataset.dir));
  });

  startBtn.addEventListener('click', startGame);

  // Initial idle frame
  resetState();
  draw();
</script>

</body>
</html>
