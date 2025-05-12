// interfaces.go                                       // Nombre del archivo.
// Ejemplo de interfaces y polimorfismo en Go          // Descripción del propósito del archivo.
package main // Declara que este archivo pertenece al paquete 'main', lo que significa que puede ser compilado como un programa ejecutable.

import "fmt" // Importa el paquete 'fmt', que proporciona funciones para formatear entrada y salida, como imprimir en la consola.

// Define una interfaz llamada 'Animal'.
// Una interfaz en Go es un conjunto de firmas de métodos.
// Cualquier tipo que implemente todos los métodos de una interfaz, implícitamente satisface esa interfaz.
type Animal interface {
	Hablar() string // Declara un método 'Hablar' que no toma argumentos y devuelve un string.
}

// Define una estructura (struct) llamada 'Perro'.
// Un struct es un tipo de dato compuesto que agrupa cero o más campos de datos.
type Perro struct{} // Perro no tiene campos de datos en este ejemplo.

// Define un método llamado 'Hablar' para el tipo 'Perro'.
// (p Perro) es el receptor del método, indica que este método pertenece al tipo 'Perro'.
// Este método implementa la firma del método 'Hablar' de la interfaz 'Animal'.
func (p Perro) Hablar() string { // El nombre del receptor 'p' es opcional y puede ser omitido si no se usa dentro del método.
	return "Guau!" // Devuelve el sonido que hace un perro.
}

// Define una estructura (struct) llamada 'Gato'.
type Gato struct{} // Gato no tiene campos de datos en este ejemplo.

// Define un método llamado 'Hablar' para el tipo 'Gato'.
// (g Gato) es el receptor del método, indica que este método pertenece al tipo 'Gato'.
// Este método también implementa la firma del método 'Hablar' de la interfaz 'Animal'.
func (g Gato) Hablar() string { // El nombre del receptor 'g' es opcional.
	return "Miau!" // Devuelve el sonido que hace un gato.
}

// Define una función llamada 'imprimirHabla' que toma un argumento 'a' del tipo 'Animal' (la interfaz).
// Esto permite que la función acepte cualquier tipo que satisfaga la interfaz 'Animal' (polimorfismo).
func imprimirHabla(a Animal) {
	// Llama al método 'Hablar()' del objeto 'a' y lo imprime en la consola.
	// fmt.Println es una función del paquete 'fmt' para imprimir una línea de texto.
	fmt.Println(a.Hablar())
}

// La función 'main' es el punto de entrada para la ejecución del programa.
func main() {
	// Declara una variable 'a' del tipo de la interfaz 'Animal'.
	var a Animal

	// Crea una instancia de 'Perro' y la asigna a la variable 'a'.
	// Como 'Perro' implementa el método 'Hablar()', es compatible con la interfaz 'Animal'.
	a = Perro{}
	// Llama a 'imprimirHabla' pasando la instancia de 'Perro' (a través de la interfaz 'Animal').
	// Se ejecutará el método 'Hablar()' específico de 'Perro'.
	imprimirHabla(a) // Salida esperada: Guau!

	// Crea una instancia de 'Gato' y la asigna a la misma variable 'a'.
	// Como 'Gato' implementa el método 'Hablar()', también es compatible con la interfaz 'Animal'.
	a = Gato{}
	// Llama a 'imprimirHabla' pasando la instancia de 'Gato' (a través de la interfaz 'Animal').
	// Se ejecutará el método 'Hablar()' específico de 'Gato'.
	imprimirHabla(a) // Salida esperada: Miau!
}
