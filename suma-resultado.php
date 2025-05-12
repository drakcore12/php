<?php
declare(strict_types=1);
// pagina2.php — Recibe valores por POST, usa vector asociativo y foreach para sumar.

header('Content-Type: text/html; charset=utf-8');

// Validamos que vengan exactamente las 5 claves esperadas
$claves = ['valor1','valor2','valor3','valor4','valor5'];
$datos  = [];
foreach ($claves as $key) {
    // filter_input con FILTER_VALIDATE_FLOAT para aceptar decimales también
    $val = filter_input(INPUT_POST, $key, FILTER_VALIDATE_FLOAT);
    if ($val === false || $val === null) {
        // Si alguno falta o no es numérico, redirigimos con error
        die("<p>Error: el campo <strong>$key</strong> debe ser un número válido.</p>");
    }
    $datos[$key] = $val;
}

// Ahora sumamos recorriendo el vector asociativo
$suma = 0.0;
foreach ($datos as $campo => $valor) {
    $suma += $valor;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Resultado de la Suma</title>
  <link rel="stylesheet" href="style.css">
  <style>
    :root {
      --result-bg: #f9f9fc;
      --result-border: var(--php-purple);
    }
    body {
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      background-color: var(--bg-light);
    }
    .container {
      background-color: var(--result-bg);
      border-left: 5px solid var(--result-border);
      border-radius: 8px;
      padding: 30px;
      max-width: 600px;
      width: 100%;
      margin: 2rem auto;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .result-title {
      color: var(--php-dark);
      text-align: center;
      margin-bottom: 25px;
      font-size: 1.8em;
    }
    .detalle {
      background-color: #f0f4f9;
      border-radius: 4px;
      padding: 20px;
      margin-bottom: 20px;
    }
    .detalle h2 {
      color: var(--php-dark);
      margin-top: 0;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 10px;
    }
    .detalle ul {
      list-style-type: none;
      padding: 0;
      margin: 0;
    }
    .detalle li {
      padding: 8px 0;
      border-bottom: 1px solid #e0e5eb;
    }
    .detalle li:last-child {
      border-bottom: none;
    }
    .resultado {
      background-color: #e9f5e9;
      border-radius: 4px;
      padding: 20px;
      text-align: center;
      font-size: 1.2em;
      color: var(--php-dark);
    }
    .navigation {
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-top: 20px;
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
  <div class="container">
    <h1 class="result-title">Resultado de la Suma</h1>

    <div class="detalle">
      <h2>Valores ingresados:</h2>
      <ul>
        <?php foreach ($datos as $campo => $valor): ?>
          <li><strong><?= htmlspecialchars($campo) ?>:</strong> <?= $valor ?></li>
        <?php endforeach; ?>
      </ul>
    </div>

    <div class="resultado">
      <p><strong>Suma total:</strong> <?= $suma ?></p>
    </div>
  </div>

  <div class="navigation">
    <a href="suma-numeros.html" class="btn-volver">&larr; Volver al formulario</a>
    <a href="index.php" class="btn-volver">&larr; Volver a la página principal</a>
  </div>
</body>
</html>
