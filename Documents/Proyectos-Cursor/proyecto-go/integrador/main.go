// main.go
// Proyecto integrador: Sistema de gestión de tareas multiusuario con API REST y cliente CLI
// Este archivo es el punto de entrada para el microservicio API REST.

// Define que este archivo pertenece al paquete 'main', indicando que es un programa ejecutable.
package main

import (
	// Importa el paquete 'encoding/json' para codificar y decodificar datos en formato JSON.
	"encoding/json"
	// Importa el paquete 'log' para funcionalidades de logging (registro de eventos).
	"log"
	// Importa el paquete 'math/rand' para generación de números pseudoaleatorios.
	"math/rand"
	// Importa el paquete 'net/http' para construir clientes y servidores HTTP.
	"net/http"
	// Importa el paquete 'sync' para primitivas de sincronización como Mutex.
	"sync"
	// Importa el paquete 'time' para funcionalidades relacionadas con el tiempo.
	"time"
)

// Usuario es una estructura que representa a un usuario del sistema.
// Los tags `json:"..."` se usan para especificar cómo los campos se mapean a JSON.
type Usuario struct {
	ID     int    `json:"id"`     // Identificador único del usuario.
	Nombre string `json:"nombre"` // Nombre del usuario.
}

// Tarea es una estructura que representa una tarea en el sistema.
type Tarea struct {
	ID          int    `json:"id"`          // Identificador único de la tarea.
	UsuarioID   int    `json:"usuario_id"`  // ID del usuario al que pertenece la tarea.
	Descripcion string `json:"descripcion"` // Descripción de la tarea.
	Completada  bool   `json:"completada"`  // Estado de la tarea (completada o no).
}

// Declaración de variables globales para almacenar los datos en memoria.
var (
	// 'usuarios' es un map que almacena objetos Usuario, usando el ID del usuario como clave.
	usuarios   = make(map[int]Usuario)
	// 'tareas' es un map que almacena objetos Tarea, usando el ID de la tarea como clave.
	tareas     = make(map[int]Tarea)
	muUsuarios sync.Mutex
	muTareas   sync.Mutex
)

func main() {
	rand.Seed(time.Now().UnixNano())
	http.HandleFunc("/usuarios", handlerUsuarios)
	http.HandleFunc("/tareas", handlerTareas)
	log.Println("API REST escuchando en :8080 ...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// CRUD Usuarios
func handlerUsuarios(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		muUsuarios.Lock()
		defer muUsuarios.Unlock()
		lista := make([]Usuario, 0, len(usuarios))
		for _, u := range usuarios {
			lista = append(lista, u)
		}
		json.NewEncoder(w).Encode(lista)
	case "POST":
		var u Usuario
		if err := json.NewDecoder(r.Body).Decode(&u); err != nil {
			http.Error(w, "JSON inválido", http.StatusBadRequest)
			return
		}
		muUsuarios.Lock()
		u.ID = rand.Intn(100000)
		usuarios[u.ID] = u
		muUsuarios.Unlock()
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(u)
	default:
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
	}
}

// CRUD Tareas
func handlerTareas(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		muTareas.Lock()
		defer muTareas.Unlock()
		lista := make([]Tarea, 0, len(tareas))
		for _, t := range tareas {
			lista = append(lista, t)
		}
		json.NewEncoder(w).Encode(lista)
	case "POST":
		var t Tarea
		if err := json.NewDecoder(r.Body).Decode(&t); err != nil {
			http.Error(w, "JSON inválido", http.StatusBadRequest)
			return
		}
		muTareas.Lock()
		t.ID = rand.Intn(100000)
		tareas[t.ID] = t
		muTareas.Unlock()
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(t)
	default:
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
	}
}
