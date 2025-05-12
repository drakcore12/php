// control.go
// Ejemplo de estructuras de control de flujo en Go

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
import "fmt"

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// if-else: Estructura de control condicional.
	// Declara e inicializa la variable 'x' con el valor 10.
	x := 10
	// Comprueba si 'x' es mayor que 5.
	if x > 5 {
		// Si la condición es verdadera, imprime "x es mayor que 5".
		fmt.Println("x es mayor que 5")
	} else {
		// Si la condición es falsa, imprime "x es menor o igual a 5".
		fmt.Println("x es menor o igual a 5")
	}

	// switch: Estructura de control para selección múltiple.
	// Declara e inicializa la variable 'color' con el valor "rojo".
	color := "rojo"
	// Evalúa el valor de 'color'.
	switch color {
	// Si 'color' es "rojo":
	case "rojo":
		// Imprime "Es rojo".
		fmt.Println("Es rojo")
	// Si 'color' es "azul":
	case "azul":
		// Imprime "Es azul".
		fmt.Println("Es azul")
	// Si ninguno de los casos anteriores coincide (cláusula default):
	default:
		// Imprime "Otro color".
		fmt.Println("Otro color")
	}

	// for: Estructura de control para bucles (iteraciones).
	// Este es un bucle for clásico con inicializador, condición y post-instrucción.
	// Inicializa 'i' a 0; el bucle continúa mientras 'i' sea menor que 3; 'i' se incrementa en 1 después de cada iteración.
	for i := 0; i < 3; i++ {
		// Imprime "Iteración" seguido del valor actual de 'i'.
		fmt.Println("Iteración", i)
	}
}
