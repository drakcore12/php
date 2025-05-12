// estructuras.go
// Ejemplo de arrays, slices, maps y structs en Go

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
import "fmt"

// Producto es una estructura (struct) que define un tipo de dato personalizado.
// Agrupa campos relacionados: Nombre (string), Precio (float64) y Stock (int).
type Producto struct {
	Nombre string  // Campo para el nombre del producto.
	Precio float64 // Campo para el precio del producto.
	Stock  int     // Campo para la cantidad en stock del producto.
}

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// Array:
	// Declara una variable 'numeros' como un array de 4 enteros.
	// Los arrays en Go tienen un tamaño fijo, especificado en la declaración ([4]int).
	// Se inicializa con los valores {10, 20, 30, 40}.
	var numeros [4]int = [4]int{10, 20, 30, 40}

	// Slice:
	// Declara e inicializa una variable 'frutas' como un slice de strings.
	// Los slices son secuencias de longitud variable que proporcionan una vista más flexible sobre los arrays.
	// Se inicializa con los valores {"manzana", "pera", "uva"}.
	frutas := []string{"manzana", "pera", "uva"}

	// Map:
	// Declara e inicializa una variable 'edades' como un map (mapa o diccionario).
	// Las claves son de tipo string y los valores son de tipo int.
	// Se inicializa con dos pares clave-valor: "Ana": 25 y "Luis": 30.
	edades := map[string]int{"Ana": 25, "Luis": 30}

	// Struct:
	// Declara e inicializa una variable 'p' del tipo Producto (la estructura definida anteriormente).
	// Se inicializan sus campos: Nombre="Laptop", Precio=999.99, Stock=5.
	p := Producto{"Laptop", 999.99, 5}

	// Imprime el contenido del array 'numeros'.
	fmt.Println("Array:", numeros)
	// Imprime el contenido del slice 'frutas'.
	fmt.Println("Slice:", frutas)
	// Imprime el contenido del map 'edades'.
	fmt.Println("Map:", edades)
	// Imprime el contenido de la instancia 'p' de Producto.
	// fmt.Println por defecto imprime los valores de los campos de un struct.
	fmt.Println("Struct:", p)
}
