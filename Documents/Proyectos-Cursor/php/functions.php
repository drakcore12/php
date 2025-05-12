<?php
declare(strict_types=1);
/**
 * functions.php
 * ----------------------------------------------------------------------------
 * Punto único de entrada para AJAX y definición de funciones "puras".
 */

// Si recibimos una acción AJAX, despachamos y salimos
if (isset($_GET["action"])) {
    header("Content-Type: application/json; charset=utf-8");

    // Sanitizar inputs
    $action = filter_input(INPUT_GET, 'action', FILTER_UNSAFE_RAW, FILTER_FLAG_STRIP_LOW | FILTER_FLAG_STRIP_HIGH) ?: '';
    $param  = filter_input(INPUT_GET, "param", FILTER_DEFAULT);

    // Funciones permitidas
    $allowed = [
        "corregirHora",
        "fibonacci",
        "esPrimo",
        "primerosPrimos",
        "generarBaloto"
    ];

    try {
        if (!in_array($action, $allowed, true) || !function_exists($action)) {
            throw new Exception("Función inválida: $action");
        }

        // Disparar función con validación de parámetros
        switch ($action) {
            case "corregirHora":
                $offset = filter_var(
                    $param,
                    FILTER_VALIDATE_INT,
                    ["options"=>["min_range"=>-12,"max_range"=>14]]
                );
                if ($offset === false) {
                    throw new Exception("Offset inválido. Debe ser -12 a +14.");
                }
                $data = corregirHora($offset);
                break;

            case "fibonacci":
                $n = filter_var(
                    $param,
                    FILTER_VALIDATE_INT,
                    ["options"=>["min_range"=>1,"max_range"=>100]]
                );
                if ($n === false) {
                    throw new Exception("Cantidad inválida. Debe ser 1 a 100.");
                }
                $data = fibonacci($n);
                break;

            case 'esPrimo':
                $num = filter_var(
                    $param,
                    FILTER_VALIDATE_INT,
                    ['options'=>['min_range'=>0]]
                );
                if ($num === false) {
                    throw new Exception("Número inválido. Debe ser un entero.");
                }
                $data = esPrimo($num);
                break;

            case "primerosPrimos":
                $cant = filter_var(
                    $param,
                    FILTER_VALIDATE_INT,
                    ["options"=>["min_range"=>1,"max_range"=>1000]]
                );
                if ($cant === false) {
                    throw new Exception("Cantidad inválida. Debe ser 1 a 1000.");
                }
                $data = primerosPrimos($cant);
                break;

            case "generarBaloto":
                $data = generarBaloto();
                break;

            default:
                throw new Exception("Operación no soportada.");
        }

        echo json_encode($data, JSON_UNESCAPED_UNICODE);
    } catch (Throwable $e) {
        http_response_code(400);
        echo json_encode(['error' => $e->getMessage()], JSON_UNESCAPED_UNICODE);
    }

    exit;
}

/* =============================================================================
   Definición de funciones "puras"
   ============================================================================= */

/**
 * Ajusta la hora de Bogotá según offset (horas) y devuelve cadena "Y-m-d H:i:s".
 */
function corregirHora(int $offset): string {
    $dt = new DateTimeImmutable("now", new DateTimeZone("America/Bogota"));
    return $dt->modify("{$offset} hours")->format("Y-m-d H:i:s");
}

/**
 * Genera los primeros $n términos de la serie de Fibonacci.
 */
function fibonacci(int $n): array {
    $seq = [];
    $a = 0;
    $b = 1;
    $used = [];
    while (count($seq) < $n) {
        if (!isset($used[$a])) {
            $seq[] = $a;
            $used[$a] = true;
        }
        $temp = $a + $b;
        $a = $b;
        $b = $temp;
    }
    return $seq;
}

/**
 * Comprueba si $num es primo (algoritmo 6k ± 1).
 */
function esPrimo(int $num): bool {
    // 0 y 1 no son primos
    if ($num < 2) {
        return false;
    }
    // 2 y 3 son primos
    if ($num === 2 || $num === 3) {
        return true;
    }
    // Números pares mayores que 2 no son primos
    if ($num % 2 === 0) {
        return false;
    }
    // Optimización para números divisibles por 3
    if ($num % 3 === 0) {
        return false;
    }
    // Algoritmo 6k ± 1 para verificar primalidad
    for ($i = 5; $i * $i <= $num; $i += 6) {
        if ($num % $i === 0 || $num % ($i + 2) === 0) {
            return false;
        }
    }
    return true;
}

/**
 * Devuelve un array con los primeros $cantidad números primos.
 */
function primerosPrimos(int $cantidad): array {
    $primos = [];
    $n = 0;
    while (count($primos) < $cantidad) {
        if (esPrimo($n)) {
            $primos[] = $n;
        }
        $n++;
    }
    return $primos;
}

/**
 * Simula Baloto: 5 números únicos (1–43) + 1 superbalota (1–16).
 */
function generarBaloto(): array {
    $nums = [];
    while (count($nums) < 5) {
        $r = random_int(1, 43);
        if (!in_array($r, $nums, true)) {
            $nums[] = $r;
        }
    }
    sort($nums);
    return [
        "balotas" => $nums,
        "super"   => random_int(1, 16)
    ];
}

// — NO cerrar la etiqueta PHP para evitar salidas accidentales —
