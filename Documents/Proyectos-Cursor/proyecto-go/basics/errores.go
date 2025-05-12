// errores.go
// Ejemplo de manejo de errores en Go

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

import (
	// Importa el paquete 'errors' para crear nuevos objetos de error.
	"errors"
	// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
	"fmt"
)

// dividir es una función que toma dos enteros 'a' y 'b'.
// Retorna un entero (el resultado de la división) y un error.
// En Go, es idiomático que las funciones que pueden fallar retornen un error como último valor.
func dividir(a, b int) (int, error) {
	// Comprueba si el divisor 'b' es cero.
	if b == 0 {
		// Si 'b' es cero, la división no es posible.
		// Retorna 0 como resultado (valor placeholder) y un nuevo error creado con errors.New().
		return 0, errors.New("no se puede dividir por cero")
	}
	// Si 'b' no es cero, realiza la división.
	// Retorna el resultado de 'a / b' y 'nil' para el error (indicando que no hubo error).
	return a / b, nil
}

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// Llama a la función 'dividir' con 10 y 0.
	// Asigna el resultado a 'resultado' y el error a 'err'.
	resultado, err := dividir(10, 0)
	// Comprueba si 'err' no es 'nil'. Si no es 'nil', significa que ocurrió un error.
	if err != nil {
		// Si hay un error, imprime "Error:" seguido del mensaje de error.
		fmt.Println("Error:", err)
	} else {
		// Si no hay error ('err' es 'nil'), imprime "Resultado:" seguido del valor de 'resultado'.
		fmt.Println("Resultado:", resultado)
	}

	// Ejemplo con una división válida para mostrar el caso sin error:
	resultadoValido, errValido := dividir(10, 2)
	// Comprueba si 'errValido' no es 'nil'.
	if errValido != nil {
		// Si hay un error, imprime el error.
		fmt.Println("Error en división válida:", errValido)
	} else {
		// Si no hay error, imprime el resultado.
		fmt.Println("Resultado división válida:", resultadoValido)
	}
}
