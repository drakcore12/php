// concurrencia.go
// Ejemplo de goroutines y canales en Go

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

import (
	// Importa el paquete 'fmt' para funcionalidades de entrada/salida.
	"fmt"
	// Importa el paquete 'time' para funcionalidades relacionadas con el tiempo, como 'Sleep'.
	"time"
)

// contar es una función que simula una tarea que toma tiempo.
// 'nombre' es un identificador para la goroutine, 'ch' es un canal de solo envío (chan<- string).
func contar(nombre string, ch chan<- string) {
	// Bucle que itera 3 veces.
	for i := 1; i <= 3; i++ {
		// Envía un mensaje formateado (string) al canal 'ch'.
		// El mensaje incluye el 'nombre' de la goroutine y el número de iteración 'i'.
		ch <- fmt.Sprintf("%s: %d", nombre, i)
		// Pausa la ejecución de esta goroutine por 500 milisegundos.
		time.Sleep(500 * time.Millisecond)
	}
	// Cierra el canal 'ch' para indicar que no se enviarán más valores.
	// Es importante cerrar los canales cuando el emisor ha terminado, para que los receptores puedan detectarlo.
	close(ch)
}

// main es la función principal donde comienza la ejecución del programa.
func main() {
	// Crea un canal de strings llamado 'ch'. Los canales se usan para la comunicación entre goroutines.
	ch := make(chan string)
	// Inicia una nueva goroutine ejecutando la función 'contar'.
	// La palabra clave 'go' ejecuta la función en una nueva goroutine (concurrente).
	// Se le pasa "Goroutine" como nombre y el canal 'ch'.
	go contar("Goroutine", ch)
	// Bucle 'for range' sobre el canal 'ch'.
	// Este bucle recibe valores del canal hasta que el canal se cierra.
	// 'msg' tomará el valor de cada string recibido del canal.
	for msg := range ch {
		// Imprime cada mensaje recibido del canal.
		fmt.Println(msg)
	}
	// Cuando el canal 'ch' se cierra y no hay más valores, el bucle 'for range' termina.
	// El programa finaliza después de que la goroutine 'main' completa su ejecución.
}
