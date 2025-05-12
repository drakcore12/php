<?php
/**
 * seccion-cuestionario.php
 * ---
 * Contiene el HTML para la sección del Quiz Interactivo.
 * Es incluido por index.php.
 * Los ejemplos de código PHP se escapan usando htmlspecialchars() para mostrarlos como texto.
 */
?>
<section id="quiz">
    <h2 class="main-section-title">Quiz Interactivo</h2>

    <!-- CARD 1: Funciones de Cadenas -->
    <div class="card">
        <h3 class="section-title">1. Funciones de Cadenas</h3>
        <p>Explora funciones como <code title="Cuenta los caracteres de una cadena">strlen()</code>, <code title="Convierte texto a mayúsculas">strtoupper()</code> y <code title="Convierte texto a minúsculas">strtolower()</code>.</p>
        <button onclick="toggleCodeVisibility(this)">Mostrar/Ocultar Ejemplo</button>
        <div class="code-container" style="display: none;">
            <pre><?php
            // Definir el código como una cadena
            $code_example_1 = '<?php
 echo strlen("Hola");       // Salida: 4
 echo strtoupper("mundo"); // Salida: MUNDO
 echo strtolower("PHP");   // Salida: php
?>';
            // Escapar y mostrar la cadena de código
            echo htmlspecialchars($code_example_1);
            ?></pre>
        </div>
        <p><strong>¿Qué función convierte a MAYÚSCULAS?</strong></p>
        <!-- Usar sr-only asume que la clase está definida en style.css para ocultarla visualmente -->
        <label for="q1_input" class="sr-only">Respuesta 1:</label>
        <input type="text" id="q1_input" aria-label="Respuesta 1" placeholder="nombreFuncion()">
        <button onclick="checkAnswer('q1_input', 'strtoupper', 'q1_feedback')">Verificar</button>
        <span id="q1_feedback" class="feedback"></span>
    </div>

    <!-- CARD 2: Manejo de Arrays -->
    <div class="card">
         <h3 class="section-title">2. Manejo de Arrays</h3>
        <p>Manipulación de arreglos: <code title="Añade elementos al final">array_push()</code>, <code title="Extrae el último elemento">array_pop()</code>, <code title="Ordena el array">sort()</code>, <code title="Cuenta elementos">count()</code>.</p>
         <button onclick="toggleCodeVisibility(this)">Mostrar/Ocultar Ejemplo</button>
         <div class="code-container" style="display: none;">
            <pre><?php
            $code_example_2 = '<?php
 $frutas = ["Manzana", "Pera"];
 array_push($frutas, "Naranja"); // Ahora es ["Manzana", "Pera", "Naranja"]
 $ultima = array_pop($frutas);  // $ultima = "Naranja", $frutas es ["Manzana", "Pera"]
 sort($frutas);                 // $frutas sigue siendo ["Manzana", "Pera"]
 echo count($frutas);            // Salida: 2
?>';
            echo htmlspecialchars($code_example_2);
            ?></pre>
        </div>
        <p><strong>¿Qué función agrega un elemento al FINAL del array?</strong></p>
        <label for="q2_input" class="sr-only">Respuesta 2:</label>
        <input type="text" id="q2_input" aria-label="Respuesta 2" placeholder="nombreFuncion()">
        <button onclick="checkAnswer('q2_input', 'array_push', 'q2_feedback')">Verificar</button>
        <span id="q2_feedback" class="feedback"></span>
    </div>

     <!-- CARD 3: date() -->
    <div class="card">
        <h3 class="section-title">3. Mostrar la Hora (Formato Simple)</h3>
        <p>Uso de <code>date()</code> para formatear y mostrar la fecha/hora actual.</p>
         <button onclick="toggleCodeVisibility(this)">Mostrar/Ocultar Ejemplo</button>
        <div class="code-container" style="display: none;">
            <pre><?php
            $code_example_3 = '<?php
 // Establecer zona horaria (importante)
 date_default_timezone_set("America/Bogota");
 // Mostrar fecha y hora formateada
 echo date("d/m/Y H:i:s"); // Ej: 25/12/2023 14:30:00
?>';
            echo htmlspecialchars($code_example_3);
            ?></pre>
        </div>
        <p><strong>¿Qué función usas para formatear y mostrar la fecha/hora?</strong></p>
        <label for="q3_input" class="sr-only">Respuesta 3:</label>
        <input type="text" id="q3_input" aria-label="Respuesta 3" placeholder="nombreFuncion()">
        <button onclick="checkAnswer('q3_input', 'date', 'q3_feedback')">Verificar</button>
        <span id="q3_feedback" class="feedback"></span>
    </div>

    <!-- CARD 4: Números Aleatorios -->
    <div class="card">
        <h3 class="section-title">4. Números Aleatorios</h3>
        <p>PHP ofrece <code title="Genera un entero aleatorio criptográficamente seguro">random_int()</code> y <code title="Genera un entero aleatorio (menos seguro)">mt_rand()</code>.</p>
        <button onclick="toggleCodeVisibility(this)">Mostrar/Ocultar Ejemplo</button>
        <div class="code-container" style="display: none;">
             <pre><?php
             $code_example_4 = '<?php
 // Recomendado para seguridad (si está disponible):
 try {
     $dadoSeguro = random_int(1, 6);
     echo "Dado seguro: $dadoSeguro";
 } catch (Exception $e) {
     echo "random_int no disponible.";
     // Fallback si random_int falla
     $dadoSeguro = mt_rand(1, 6);
 }

 // Más rápido, menos seguro, pero ampliamente disponible:
 $dadoRapido = mt_rand(1, 6);
 echo "\nDado rápido: $dadoRapido";
?>';
             echo htmlspecialchars($code_example_4);
             ?></pre>
        </div>
        <p><strong>¿Qué función PHP recomendada genera números aleatorios seguros?</strong></p>
        <label for="q4_input" class="sr-only">Respuesta 4:</label>
        <input type="text" id="q4_input" aria-label="Respuesta 4" placeholder="nombreFuncion()">
        <button onclick="checkAnswer('q4_input', 'random_int', 'q4_feedback')">Verificar</button>
        <span id="q4_feedback" class="feedback"></span>
    </div>

     <!-- CARD 5: Superglobal $_POST -->
    <div class="card">
        <h3 class="section-title">5. Procesar Formularios (POST)</h3>
        <p>Se usa la variable superglobal <code>$_POST</code> para acceder a datos enviados vía <code>method="POST"</code>.</p>
        <button onclick="toggleCodeVisibility(this)">Mostrar/Ocultar Ejemplo</button>
        <div class="code-container" style="display: none;">
           <pre><?php
           $code_example_5 = '<!-- HTML del formulario -->
<form method="POST" action="procesar.php">
  <label for="username">Usuario:</label>
  <input type="text" id="username" name="username">
  <button type="submit">Enviar</button>
</form>

<?php
 // --- En el archivo procesar.php ---
 if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Acceder al dato enviado. Usar ?? para valor por defecto si no llega.
    $user = $_POST["username"] ?? \'Invitado\';

    // ¡IMPORTANTE! Siempre sanitizar/validar datos del usuario.
    // htmlspecialchars previene XSS al mostrarlo.
    echo "Hola, " . htmlspecialchars($user);
 }
?>';
           echo htmlspecialchars($code_example_5);
           ?></pre>
        </div>
         <p><strong>¿Con qué variable superglobal accedes a los datos enviados por <code>method="POST"</code>?</strong></p>
        <label for="q5_input" class="sr-only">Respuesta 5:</label>
        <input type="text" id="q5_input" aria-label="Respuesta 5" placeholder="$_VARIABLE">
        <button onclick="checkAnswer('q5_input', '$_POST', 'q5_feedback')">Verificar</button>
        <span id="q5_feedback" class="feedback"></span>
    </div>

</section> <!-- Fin Sección Quiz -->