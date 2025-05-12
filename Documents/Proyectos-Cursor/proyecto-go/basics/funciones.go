// funciones.go
// Ejemplo de funciones y métodos en Go, con explicaciones detalladas.

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
import "fmt"

// suma es una función simple que recibe dos enteros (a, b) y retorna su suma como un entero.
// Las funciones en Go se definen con la palabra clave 'func'.
// Los tipos de los parámetros (a int, b int) y el tipo de retorno (int) se especifican.
func suma(a int, b int) int {
	// El valor de retorno se indica después de los parámetros.
	// Esta línea calcula la suma de 'a' y 'b' y la devuelve.
	return a + b
}

// dividir es una función que retorna dos valores: el cociente y el resto de una división entera.
// Go permite retornar múltiples valores de una función.
// Los parámetros son 'dividendo' y 'divisor', ambos enteros.
// Los tipos de los valores de retorno son (int, int).
func dividir(dividendo, divisor int) (int, int) {
	// Retorna el resultado de la división entera (dividendo / divisor)
	// y el resto de la división entera (dividendo % divisor).
	return dividendo / divisor, dividendo % divisor
}

// Persona es una estructura (struct) que agrupa datos bajo un mismo tipo.
// Los structs permiten crear tipos personalizados con uno o más campos.
type Persona struct {
	// Nombre es un campo de la estructura Persona, de tipo string.
	Nombre string
}

// Saludar es un método asociado al tipo Persona.
// Un método es una función que tiene un "receptor" (en este caso, 'p Persona').
// El receptor 'p' es una instancia del tipo Persona sobre la cual opera el método.
func (p Persona) Saludar() {
	// Imprime un saludo utilizando el campo Nombre de la instancia 'p' de Persona.
	fmt.Println("Hola, soy", p.Nombre)
}

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// Uso de la función suma:
	// Llama a la función 'suma' con los argumentos 2 y 3.
	// Imprime la cadena "Suma:" seguida del resultado devuelto por 'suma'.
	fmt.Println("Suma:", suma(2, 3))

	// Uso de función con retorno múltiple:
	// Llama a la función 'dividir' con los argumentos 7 y 3.
	// Asigna los dos valores retornados a las variables 'cociente' y 'resto' respectivamente.
	cociente, resto := dividir(7, 3)
	// Imprime la cadena "División:", seguida del valor de 'cociente', la cadena "resto:", y el valor de 'resto'.
	fmt.Println("División:", cociente, "resto:", resto)

	// Creación de una instancia de Persona y uso de su método:
	// Crea una instancia de la estructura Persona, inicializando el campo Nombre con "Ana".
	// La variable 'p' ahora contiene esta instancia.
	p := Persona{"Ana"}
	// Llama al método Saludar() sobre la instancia 'p'.
	p.Saludar()
}
