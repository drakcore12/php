// paquetes.go
// Ejemplo de organización en paquetes en Go
// Este archivo solo muestra cómo se declara un paquete y cómo importar otro paquete.
// Para ejecutar ejemplos de paquetes, crea subcarpetas y archivos con funciones exportadas.

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

import (
	// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
	"fmt"
	// Importa un paquete personalizado llamado 'mipaquete'.
	// Para que esto funcione, debe existir una carpeta llamada 'mipaquete'
	// en una ubicación que Go pueda encontrar (por ejemplo, dentro del mismo proyecto,
	// o en el GOPATH/GOROOT si se configura así).
	// El nombre 'mipaquete' aquí se refiere al nombre del directorio.
	// Si el archivo `main.go` está en `proyecto-go/basics/paquetes.go`
	// y `mipaquete` está en `proyecto-go/mipaquete/mipaquete.go`,
	// la importación sería "nombre_modulo/mipaquete" si usas Go Modules.
	// Asumiendo que 'mipaquete' está en una ruta de importación válida.
	// Por ejemplo, si tu módulo se llama 'proyecto-go' y 'mipaquete' está en la raíz:
	// import "proyecto-go/mipaquete"
	// Para este ejemplo simple, asumimos que 'mipaquete' está configurado para ser encontrado.
	// Si 'mipaquete' está en la misma carpeta 'basics', la importación sería incorrecta.
	// Go busca paquetes en $GOROOT/src y $GOPATH/src o usando Go Modules.
	// Para un ejemplo local simple, si creas `proyecto-go/mipaquete/codigo.go` con `package mipaquete`,
	// y tu `go.mod` está en `proyecto-go` definiendo `module mi_proyecto_principal`,
	// la importación sería `mi_proyecto_principal/mipaquete`.
	// Para este ejemplo, vamos a asumir que el paquete 'mipaquete' está accesible.
	// El comentario original sugiere crear una carpeta 'mipaquete' con 'mipaquete.go' dentro.
	// Si `proyecto-go` es la raíz del módulo, y creas `proyecto-go/mipaquete/mipaquete.go`,
	// y `go.mod` en `proyecto-go` dice `module ejemplo.com/proyecto-go`,
	// entonces la importación sería `ejemplo.com/proyecto-go/mipaquete`.
	// Para simplificar, si 'mipaquete' es un directorio al mismo nivel que 'basics' y 'integrador',
	// y 'proyecto-go' es la raíz del módulo (ej: `module miproject`),
	// la importación sería `miproject/mipaquete`.
	// Dado el contexto, es probable que 'mipaquete' sea un directorio hermano de 'basics'.
	"mipaquete" // Esta línea asume que 'mipaquete' es un paquete accesible.
)

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// Llama a la función 'Mensaje' del paquete 'mipaquete'.
	// Las funciones exportadas de otros paquetes comienzan con mayúscula.
	// Imprime el string devuelto por mipaquete.Mensaje().
	fmt.Println(mipaquete.Mensaje())
}

// Comentario original del archivo, útil para entender la estructura esperada:
// Crea una carpeta llamada mipaquete con un archivo mipaquete.go:
// package mipaquete
// func Mensaje() string { return "¡Hola desde un paquete!" }
// Para que este ejemplo funcione, deberías tener una estructura así (asumiendo que `proyecto-go` es tu módulo):
// proyecto-go/
//   go.mod  (con `module <nombre_del_modulo>`)
//   basics/
//     paquetes.go
//   mipaquete/
//     mipaquete.go (con `package mipaquete` y `func Mensaje() ...`)
// Y la importación en paquetes.go sería `<nombre_del_modulo>/mipaquete`
