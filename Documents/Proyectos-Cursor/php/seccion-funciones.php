<?php
/**
 * seccion-funciones.php
 * ----------------------------------------------------------------------------
 * Sección HTML que muestra tarjetas para cada función interactiva.
 */
?>
<section id="funciones" class="functions-section">
  <h2 class="main-section-title">Funciones PHP Interactivas</h2>

  <?php
  $cards = [
    [
      "fn"     => "corregirHora",
      "label"  => "Offset (horas) [-12..+14]",
      "type"   => "number",
      "attrs"  => ["min"=>-12,"max"=>14,"value"=>0],
      "desc"   => "Devuelve hora UTC ajustada por offset"
    ],
    [
      "fn"     => "fibonacci",
      "label"  => "Términos (1..100)",
      "type"   => "number",
      "attrs"  => ["min"=>1,"max"=>100,"value"=>10],
      "desc"   => "Genera serie de Fibonacci"
    ],
    [
      "fn"     => "esPrimo",
      "label"  => "Número (≥0)",
      "type"   => "number",
      "attrs"  => ["min"=>0,"value"=>0],
      "desc"   => "¿Es primo? true/false"
    ],
    [
      "fn"     => "primerosPrimos",
      "label"  => "Cantidad (1..1000)",
      "type"   => "number",
      "attrs"  => ["min"=>1,"max"=>1000,"value"=>15],
      "desc"   => "Listado de primeros N primos"
    ],
    [
      "fn"     => "generarBaloto",
      "label"  => "",
      "type"   => null,
      "attrs"  => [],
      "desc"   => "Sorteo Baloto completo"
    ],
    [
      "fn"     => "sumadora",
      "label"  => "",
      "type"   => null,
      "attrs"  => [],
      "desc"   => "Sumadora de 5 números (POST)",
      "link"   => "suma-numeros.html"
    ],
    [
      "fn"     => "calculadora",
      "label"  => "",
      "type"   => null,
      "attrs"  => [],
      "desc"   => "Calculadora con múltiples operaciones",
      "link"   => "calculadora-cientifica.php"
    ],
  ];

  foreach ($cards as $c):
  ?>
    <div class="card function-card">
      <h3 class="section-title"><code><?= $c["fn"] ?>()</code></h3>
      <p><?= $c["desc"] ?></p>

      <?php if ($c["type"]): ?>
        <label for="param_<?= $c["fn"] ?>" class="sr-only"><?= $c["label"] ?></label>
        <input
          type="<?= $c["type"] ?>"
          id="param_<?= $c["fn"] ?>"
          <?php foreach ($c["attrs"] as $k => $v) echo "{$k}=\"{$v}\" "; ?>
          placeholder="<?= $c["label"] ?>"
        >
      <?php endif; ?>

      <?php if (isset($c['link']) && in_array($c['fn'], ['sumadora', 'calculadora'])): ?>
        <a href="<?= $c['link'] ?>" class="execute-btn redirect-btn">
          <span>Ir</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
          </svg>
        </a>
      <?php elseif (!isset($c['link'])): ?>
        <button
          class="execute-btn"
          onclick="executeFunction(
             this,
             '<?= $c['fn'] ?>',
             'result_<?= $c['fn'] ?>'
             <?= $c['type'] ? ", 'param_" . $c['fn'] . "'" : '' ?>
           )"
        >Ejecutar</button>
      <?php endif; ?>

      <?php if (!in_array($c['fn'], ['sumadora', 'calculadora'])): ?>
        <pre id="result_<?= $c["fn"] ?>" class="result">Sin ejecutar.</pre>
      <?php endif; ?>
    </div>
  <?php endforeach; ?>
</section>
