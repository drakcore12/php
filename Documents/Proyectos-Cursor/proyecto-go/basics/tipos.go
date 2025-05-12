// tipos.go
// Ejemplo de tipos de datos básicos y compuestos en Go

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
import "fmt"

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// Tipos básicos:
	// Declara una variable 'entero' de tipo 'int' y la inicializa con 42.
	var entero int = 42
	// Declara una variable 'decimal' de tipo 'float64' (número de punto flotante de doble precisión) y la inicializa con 3.14.
	var decimal float64 = 3.14
	// Declara una variable 'booleano' de tipo 'bool' y la inicializa con 'true'.
	var booleano bool = true
	// Declara una variable 'texto' de tipo 'string' y la inicializa con "Hola, Go!".
	var texto string = "Hola, Go!"

	// Tipos compuestos:
	// Declara una variable 'arreglo' de tipo array de 3 enteros y la inicializa con los valores {1, 2, 3}.
	// Los arrays en Go tienen un tamaño fijo.
	var arreglo [3]int = [3]int{1, 2, 3}
	// Declara una variable 'slice' e la inicializa con un slice de strings {"a", "b", "c"}.
	// Los slices son secuencias de longitud variable que referencian a un array subyacente.
	slice := []string{"a", "b", "c"}
	// Declara una variable 'mapeo' e la inicializa con un map (diccionario o tabla hash).
	// Las claves son strings y los valores son enteros.
	mapeo := map[string]int{"uno": 1, "dos": 2}

	// Imprime el valor de la variable 'entero' precedido por "Entero:".
	fmt.Println("Entero:", entero)
	// Imprime el valor de la variable 'decimal' precedido por "Decimal:".
	fmt.Println("Decimal:", decimal)
	// Imprime el valor de la variable 'booleano' precedido por "Booleano:".
	fmt.Println("Booleano:", booleano)
	// Imprime el valor de la variable 'texto' precedido por "Texto:".
	fmt.Println("Texto:", texto)
	// Imprime el valor de la variable 'arreglo' precedido por "Arreglo:".
	fmt.Println("Arreglo:", arreglo)
	// Imprime el valor de la variable 'slice' precedido por "Slice:".
	fmt.Println("Slice:", slice)
	// Imprime el valor de la variable 'mapeo' precedido por "Map:".
	fmt.Println("Map:", mapeo)
}
