<?php
/**
 * index.php
 * ---
 * Archivo principal para la aplicación "PHP para Aprender".
 * Incluye funciones, estructura HTML base, secciones de contenido y JavaScript.
 */

// --- Configuración de Errores (solo en desarrollo) ---
error_reporting(E_ALL);
ini_set('display_errors', '1');

// --- Incluir funciones y manejo AJAX antes de cualquier salida HTML ---
require_once 'functions.php';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP para Aprender</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>
    <header>
        <h1>PHP para Aprender</h1>
    </header>

    <nav role="navigation">
        <ul class="nav-list">
            <li><a href="#codigo">Código de Ejemplo</a></li>
            <li><a href="#funciones">Funciones Interactivas</a></li>
        </ul>
    </nav>

    <main class="container">
        <!-- Sección de Código de Ejemplo (Quiz) -->
        <?php
            if (file_exists('seccion-cuestionario.php')) {
                include 'seccion-cuestionario.php';
            } else {
                echo "<p class='error'>Error: no se encontró <code>seccion-cuestionario.php</code>.</p>";
            }
        ?>

        <!-- Sección de Funciones PHP Interactivas -->
        <?php
            if (file_exists('seccion-funciones.php')) {
                include 'seccion-funciones.php';
            } else {
                echo "<p class='error'>Error: no se encontró <code>seccion-funciones.php</code>.</p>";
            }
        ?>
    </main>

    <footer>
        © <?php echo date('Y'); ?> Miguel Ángel Noreña Cano – PHP para Aprender
    </footer>

    <script>
    // ---------------------------------------------------------
    // Función: toggleCodeVisibility
    // Muestra/oculta ejemplos de código en el Quiz
    // ---------------------------------------------------------
    function toggleCodeVisibility(button) {
        const codeContainer = button.nextElementSibling;
        if (codeContainer && codeContainer.classList.contains('code-container')) {
            const hidden = codeContainer.style.display === 'none' || codeContainer.style.display === '';
            codeContainer.style.display = hidden ? 'block' : 'none';
            button.textContent = hidden ? 'Ocultar Ejemplo' : 'Mostrar Ejemplo';
        } else {
            console.error('No se encontró .code-container junto al botón.', button);
        }
    }

    // ---------------------------------------------------------
    // Función: checkAnswer
    // Verifica respuestas del Quiz comparando con la respuesta correcta
    // ---------------------------------------------------------
    function checkAnswer(inputId, correctAnswer, feedbackId) {
        const answerInput = document.getElementById(inputId);
        const feedbackSpan = document.getElementById(feedbackId);
        if (!answerInput || !feedbackSpan) {
            console.error('checkAnswer: elemento no encontrado', { inputId, feedbackId });
            return;
        }
        const user = answerInput.value.trim().toLowerCase().replace(/\(\)\s*$/, '');
        const correct = correctAnswer.toLowerCase().replace(/\(\)\s*$/, '');
        if (user === correct) {
            feedbackSpan.textContent = '¡Correcto!';
            feedbackSpan.className = 'feedback feedback-correct';
        } else {
            feedbackSpan.textContent = 'Incorrecto. La respuesta es: ' + correctAnswer;
            feedbackSpan.className = 'feedback feedback-incorrect';
        }
    }

    // ---------------------------------------------------------
    // Función: executeFunction
    // Llama a tus funciones PHP vía AJAX y muestra el resultado
    // ---------------------------------------------------------
    function executeFunction(button, functionName, resultDivId, paramInputId) {
        const resultDiv = document.getElementById(resultDivId);
        if (!resultDiv) {
            console.error('executeFunction: div de resultado no encontrado', resultDivId);
            return;
        }
        let paramValue = '';
        if (paramInputId) {
            const inp = document.getElementById(paramInputId);
            paramValue = inp ? inp.value.trim() : '';
        }
        resultDiv.textContent = 'Ejecutando...';
        resultDiv.classList.add('loading');
        button.disabled = true;
        const url = `?action=${encodeURIComponent(functionName)}` +
                    (paramValue ? `&param=${encodeURIComponent(paramValue)}` : '');
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(text => {
                // Trim any potential HTML or whitespace
                const cleanText = text.replace(/<[^>]*>/g, '').trim();
                resultDiv.textContent = cleanText || 'Sin resultado';
                resultDiv.classList.remove('loading');
                // Highlight error messages
                if (cleanText.startsWith('Error:')) {
                    resultDiv.classList.add('feedback-incorrect');
                } else {
                    resultDiv.classList.remove('feedback-incorrect');
                }
            })
            .catch(err => {
                console.error('Fetch error:', err);
                resultDiv.textContent = 'Error de conexión: ' + err.message;
                resultDiv.classList.add('feedback-incorrect');
            })
            .finally(() => {
                button.disabled = false;
            });
    }
    </script>
</body>
</html>
