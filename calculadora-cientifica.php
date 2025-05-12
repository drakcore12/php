<?php
// index.php — Calculadora Científica Avanzada en un solo archivo PHP
// Solo usamos PHP para servir el HTML; toda la lógica de cálculo es cliente-side con math.js
session_start();
?><!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Calculadora Científica Avanzada</title>
  <!-- math.js para parsing y cálculo de expresiones -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.11.0/math.min.js"></script>
    <style>
    /* ========== Reset y diseño base ========== */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #f0f2f5;
      color: #6c757d;
      font-family: sans-serif;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
      padding: 2rem;
    }

    /* tarjeta con fade-in */
    .calculator {
      background: #ffffff;
      border-radius: 8px;
      padding: 1rem;
      width: 380px;
      box-shadow: 0 8px 16px rgba(0,0,0,0.1);
      animation: fadeIn 0.4s ease-out;
    }

    /* display con sombra interior */
    #display {
      width: 100%;
      height: 50px;
      font-size: 1.5rem;
      text-align: right;
      padding: .5rem;
      border-radius: 4px;
      border: none;
      margin-bottom: .5rem;
      background: #2d2d2d;
      color: #e6e6e6;
      box-shadow: inset 0 -4px 6px rgba(0,0,0,0.2);
      transition: background .2s;
    }

    .buttons {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: .4rem;
    }

    /* botones base con sombra y transición */
    .button {
      background: #8892be;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: .6rem;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 4px 8px rgba(0,0,0,0.2);
      transition: transform .1s ease, box-shadow .2s ease, background .2s;
    }
    .button:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .button:active {
      transform: scale(0.97);
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* variaciones por tipo */
    .button.operator { background: #4F5B93; }
    .button.memory   { background: #007bff; }
    .button.action   { background: #dc3545; }
    .button.action[data-action="calculate"] {
      background: #28a745;
      color: #fff;
    }

    /* historial con sombra interior */
    .history {
      margin-top: 1rem;
      background: #ffffff;
      border-radius: 4px;
      padding: .5rem;
      max-height: 140px;
      overflow-y: auto;
      font-size: .85rem;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    .history ul { list-style: none; }
    .history li { margin-bottom: .3rem; }

    /* keyframes fadeIn */
    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.95); }
      to   { opacity: 1; transform: scale(1); }
    }

    /* Navegación */
    .navigation {
      position: fixed;
      bottom: 20px;
      left: 0;
      width: 100%;
      text-align: center;
      z-index: 1000;
    }
    .btn-volver {
      color: var(--php-dark);
      text-decoration: none;
      font-weight: 600;
      transition: color 0.3s ease;
    }
    .btn-volver:hover {
      color: var(--php-purple);
      text-decoration: underline;
    }
  </style>

</head>
<body>
  <div class="calculator">
    <input type="text" id="display" readonly value="0">

    <div class="buttons">
      <!-- Memoria e historial -->
      <button class="button memory" data-action="mc">MC</button>
      <button class="button memory" data-action="mr">MR</button>
      <button class="button memory" data-action="m-plus">M+</button>
      <button class="button memory" data-action="m-minus">M-</button>
      <button class="button memory" data-action="ms">MS</button>
      <button class="button action" data-action="clear-history">Hist</button>

      <!-- Borrado y entrada -->
      <button class="button action" data-action="clear">C</button>
      <button class="button action" data-action="clear-entry">CE</button>
      <button class="button action" data-action="back">←</button>
      <button class="button" data-value="(">(</button>
      <button class="button" data-value=")">)</button>
      <button class="button action" data-action="ans">Ans</button>

      <!-- Funciones científicas -->
      <button class="button operator" data-value="sin(">sin</button>
      <button class="button operator" data-value="cos(">cos</button>
      <button class="button operator" data-value="tan(">tan</button>
      <button class="button operator" data-value="abs(">abs</button>
      <button class="button operator" data-value="log10(">log</button>
      <button class="button operator" data-value="log(">ln</button>

      <!-- Más operadores avanzados -->
      <button class="button operator" data-value="sqrt(">√</button>
      <button class="button operator" data-value="nthRoot(">ⁿ√</button>
      <button class="button operator" data-value="^">^</button>
      <button class="button operator" data-value="!">n!</button>
      <button class="button operator" data-value="mod(">mod</button>
      <button class="button operator" data-value="%">%</button>

      <!-- Constantes y exponencial -->
      <button class="button operator" data-value="pi">π</button>
      <button class="button operator" data-value="e">e</button>
      <button class="button operator" data-value="exp(">exp</button>
      <div></div><div></div><div></div>

      <!-- Números y operadores básicos -->
      <button class="button" data-value="7">7</button>
      <button class="button" data-value="8">8</button>
      <button class="button" data-value="9">9</button>
      <button class="button operator" data-value="/">÷</button>
      <button class="button operator" data-value="*">×</button>
      <button class="button action" data-action="calculate">=</button>

      <button class="button" data-value="4">4</button>
      <button class="button" data-value="5">5</button>
      <button class="button" data-value="6">6</button>
      <button class="button operator" data-value="-">−</button>
      <button class="button operator" data-value="+">+</button>
      <div></div>

      <button class="button" data-value="1">1</button>
      <button class="button" data-value="2">2</button>
      <button class="button" data-value="3">3</button>
      <button class="button" data-value="0">0</button>
      <button class="button" data-value=".">.</button>
      <div></div>
    </div>

    <!-- Panel de historial -->
    <div class="history">
      <ul id="history"></ul>
    </div>
  </div>
  
  <div class="navigation">
    <a href="index.php" class="btn-volver">&larr; Volver a la página principal</a>
  </div>

  <script>
    // Referencias DOM
    const display     = document.getElementById('display');
    const historyList = document.getElementById('history');

    // Recuperar memoria e historial de localStorage
    let memory = parseFloat(localStorage.getItem('calc_memory')) || 0;
    let ans    = parseFloat(localStorage.getItem('calc_ans')) || 0;
    const history = JSON.parse(localStorage.getItem('calc_history')) || [];

    // Refrescar historial en pantalla
    function updateHistory() {
      historyList.innerHTML = '';
      history.slice(-20).reverse().forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        historyList.appendChild(li);
      });
      localStorage.setItem('calc_history', JSON.stringify(history));
    }
    updateHistory();

    // Ejecutar cálculo con math.js
    function calculate() {
      const expr = display.value;
      if (!expr) return;
      try {
        const result = math.evaluate(expr);
        ans = result;
        history.push(`${expr} = ${result}`);
        localStorage.setItem('calc_ans', ans);
        updateHistory();
        display.value = result;
      } catch {
        display.value = 'Error';
      }
    }

    // Manejador de botones
    document.querySelectorAll('.button').forEach(btn => {
      btn.addEventListener('click', () => {
        const v = btn.dataset.value;
        const action = btn.dataset.action;

        if (v !== undefined) {
          // Inserta valor o reemplaza tras "Error" o "0"
          if (display.value === '0' || display.value === 'Error') {
            display.value = v;
          } else {
            display.value += v;
          }
        } else if (action) {
          switch (action) {
            case 'clear':
              display.value = '0';
              break;
            case 'clear-entry':
              display.value = '';
              break;
            case 'back':
              display.value = display.value.slice(0, -1) || '0';
              break;
            case 'calculate':
              calculate();
              break;
            case 'mc':
              memory = 0;
              localStorage.setItem('calc_memory', memory);
              break;
            case 'mr':
              display.value = (display.value==='0' || display.value==='Error') 
                               ? memory 
                               : display.value + memory;
              break;
            case 'ms':
              memory = parseFloat(display.value) || 0;
              localStorage.setItem('calc_memory', memory);
              break;
            case 'm-plus':
              memory += parseFloat(display.value) || 0;
              localStorage.setItem('calc_memory', memory);
              break;
            case 'm-minus':
              memory -= parseFloat(display.value) || 0;
              localStorage.setItem('calc_memory', memory);
              break;
            case 'ans':
              display.value = (display.value==='0' || display.value==='Error') 
                               ? ans 
                               : display.value + ans;
              break;
            case 'clear-history':
              history.length = 0;
              updateHistory();
              break;
          }
        }
      });
    });
  </script>
</body>
</html>
