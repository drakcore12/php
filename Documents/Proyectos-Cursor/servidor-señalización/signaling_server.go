package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	"golang.org/x/crypto/bcrypt"
)

// Funciones de validación
func isValidUsername(username string) bool {
	valid, _ := regexp.MatchString(`^[a-zA-Z0-9_-]{3,20}$`, username)
	return valid
}

func isStrongPassword(pwd string) bool {
	if len(pwd) < 6 {
		return false
	}
	hasLetter := strings.ContainsAny(pwd, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
	hasNumber := strings.ContainsAny(pwd, "0123456789")
	return hasLetter && hasNumber
}

// Estructuras de datos
type Client struct {
	Username string
	Conn     *websocket.Conn
}

type Server struct {
	clients    map[string]*Client
	clientsMux sync.Mutex
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

// Funciones de base de datos
func execSQLQuery(query string) (string, error) {
	cmd := exec.Command("sqlcmd",
		"-S", `np:\\.\pipe\LOCALDB#65A3AC87\tsql\query`, // Corregido: Eliminado el espacio inicial
		"-d", "Chatp2pDB",
		"-Q", query,
		"-W",
		"-s", "|",
	)
	out, err := cmd.CombinedOutput()
	return string(out), err
}

func userExists(username string) bool {
	username = strings.TrimSpace(username)
	username = strings.ReplaceAll(username, "'", "''")
	query := fmt.Sprintf(`SELECT COUNT(*) FROM Users WHERE username = '%s'`, username)
	out, err := execSQLQuery(query)
	if err != nil {
		log.Printf("Error ejecutando userExists: %v", err)
		return false
	}

	re := regexp.MustCompile(`(?m)^\s*([01])\s*$`)
	match := re.FindStringSubmatch(out)
	if len(match) == 2 {
		log.Printf("userExists count result: %s", match[1])
		return match[1] != "0"
	}
	log.Printf("userExists: respuesta inesperada:\n%s", out)
	return false
}

func registerUser(username, password string) error {
	username = strings.ReplaceAll(username, "'", "''")
	username = strings.TrimSpace(username)
	password = strings.TrimSpace(password)

	if username == "" || password == "" {
		return fmt.Errorf("username o password vacío")
	}

	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return fmt.Errorf("error creando hash: %v", err)
	}

	query := fmt.Sprintf(`INSERT INTO Users(username, password_hash) VALUES('%s', '%s')`, username, string(hash))
	log.Printf("📝 Ejecutando registro SQL: %s", query)
	_, err = execSQLQuery(query)
	return err
}

func getUserPasswordHash(username string) (string, error) {
	username = strings.ReplaceAll(username, "'", "''")
	query := fmt.Sprintf(`SELECT password_hash FROM Users WHERE username = '%s'`, username)
	out, err := execSQLQuery(query)
	if err != nil {
		return "", err
	}
	lines := strings.Split(out, "\n")
	if len(lines) < 3 {
		return "", fmt.Errorf("no result")
	}
	return strings.TrimSpace(lines[2]), nil
}

// Funciones del servidor
func NewServer() *Server {
	return &Server{clients: make(map[string]*Client)}
}

func (s *Server) handleWS(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}
	defer conn.Close()

	var username string
	for {
		var init map[string]string
		if err := conn.ReadJSON(&init); err != nil {
			return
		}
		switch init["type"] {
		case "register":
			user := init["username"]
			pass := init["password"]
			user = strings.TrimSpace(user)
			pass = strings.TrimSpace(pass)

			if user == "" || pass == "" {
				conn.WriteJSON(map[string]string{"type": "register-failed", "message": "usuario o contraseña vacíos"})
				continue
			}
			if !isValidUsername(user) {
				conn.WriteJSON(map[string]string{"type": "register-failed", "message": "nombre inválido (solo letras, números, guiones, 3-20 caracteres)"})
				continue
			}

			if userExists(user) {
				conn.WriteJSON(map[string]string{"type": "register-failed", "message": "usuario ya existe"})
				continue
			}

			if !isStrongPassword(pass) {
				conn.WriteJSON(map[string]string{"type": "register-failed", "message": "la contraseña debe tener mínimo 6 caracteres, incluyendo letras y números"})
				continue
			}

			if err := registerUser(user, pass); err != nil {
				log.Printf("❌ Error al registrar: %v", err)
				conn.WriteJSON(map[string]string{"type": "register-failed", "message": "error al insertar en la base de datos"})
				continue
			}

			conn.WriteJSON(map[string]string{"type": "register-success"})
			log.Printf("🟢 Usuario registrado: %s", user)

		case "login":
			user := strings.TrimSpace(init["username"])
			pass := strings.TrimSpace(init["password"])

			if user == "" || pass == "" {
				conn.WriteJSON(map[string]string{"type": "login-failed", "message": "usuario o contraseña vacíos"})
				continue
			}

			hash, err := getUserPasswordHash(user)
			if err != nil || bcrypt.CompareHashAndPassword([]byte(hash), []byte(pass)) != nil {
				conn.WriteJSON(map[string]string{"type": "login-failed", "message": "invalid creds"})
				continue
			}
			username = user
			s.clientsMux.Lock()
			s.clients[user] = &Client{Username: user, Conn: conn}
			s.clientsMux.Unlock()
			conn.WriteJSON(map[string]string{"type": "login-success"})
			log.Printf("🔑 Usuario inició sesión: %s", user)

			log.Printf("User connected: %s", user)
			s.broadcastUserList()
			goto mainLoop
		default:
			conn.WriteJSON(map[string]string{"type": "error", "message": "must register or login"})
		}
	}

mainLoop:
	for {
		var msg map[string]interface{}
		if err := conn.ReadJSON(&msg); err != nil {
			log.Printf("🔌 Error leyendo mensaje JSON: %v", err)
			break
		}

		log.Printf("🧾 Mensaje recibido en servidor: %+v", msg)

		switch msg["type"] {
		case "list-users":
			s.sendUserListTo(username)

		case "text", "signal":
			to, ok := msg["to"].(string)
			if !ok || to == "" {
				log.Printf("⚠️ Campo 'to' inválido o ausente: %+v", msg)
				break
			}

			s.clientsMux.Lock()
			dest, ok := s.clients[to]
			s.clientsMux.Unlock()

			if !ok {
				log.Printf("❌ Destinatario %s no está conectado", to)
				break
			}

			log.Printf("📤 Reenviando mensaje a %s: %+v", to, msg)

			// Guardar mensaje en la base de datos si es de tipo "text"
			if msg["type"] == "text" {
				from, _ := msg["from"].(string)
				content, _ := msg["content"].(string)
				if err := saveMessage(from, to, content); err != nil {
					log.Printf("❌ Error guardando mensaje en DB: %v", err)
				}

				// Crear estructura Message con formato correcto
				serverMsg := map[string]interface{}{
					"from":      from,
					"to":        to,
					"content":   content,
					"type":      "text",
					"timestamp": time.Now().Format(time.RFC3339),
				}

				jsonMsg, err := json.Marshal(serverMsg)
				if err != nil {
					log.Printf("❌ Error al serializar mensaje para %s: %v", to, err)
					break
				}

				err = dest.Conn.WriteMessage(websocket.TextMessage, jsonMsg)
				if err != nil {
					log.Printf("❌ Error al enviar mensaje a %s: %v", to, err)
				}
				continue
			}

			// Para mensajes de tipo "signal", mantener el formato original
			jsonMsg, err := json.Marshal(msg)
			if err != nil {
				log.Printf("❌ Error al serializar mensaje para %s: %v", to, err)
				break
			}

			err = dest.Conn.WriteMessage(websocket.TextMessage, jsonMsg)
			if err != nil {
				log.Printf("❌ Error al enviar mensaje a %s: %v", to, err)
			}
		}
	}

	// Al salir del bucle principal: limpiar cliente
	s.clientsMux.Lock()
	delete(s.clients, username)
	s.clientsMux.Unlock()
	log.Printf("🔴 Usuario desconectado: %s", username)

	s.broadcastUserList()

	// Eliminar estas líneas duplicadas:
	// s.clientsMux.Lock()
	// delete(s.clients, username)
	// s.clientsMux.Unlock()
	// log.Printf("User disconnected: %s", username)
	// log.Printf("🔴 Usuario desconectado: %s", username)

	// s.broadcastUserList()
}

func (s *Server) broadcastUserList() {
	s.clientsMux.Lock()
	defer s.clientsMux.Unlock()
	users := make([]string, 0, len(s.clients))
	for u := range s.clients {
		users = append(users, u)
	}
	payload := map[string]interface{}{"type": "user-list", "users": users}
	for _, c := range s.clients {
		c.Conn.WriteJSON(payload)
	}
}

func (s *Server) sendUserListTo(user string) {
	s.clientsMux.Lock()
	defer s.clientsMux.Unlock()
	c, ok := s.clients[user]
	if !ok {
		return
	}
	users := make([]string, 0, len(s.clients))
	for u := range s.clients {
		users = append(users, u)
	}
	c.Conn.WriteJSON(map[string]interface{}{"type": "user-list", "users": users})
}

func saveMessage(from, to, content string) error {
	from = strings.ReplaceAll(from, "'", "''")
	to = strings.ReplaceAll(to, "'", "''")
	content = strings.ReplaceAll(content, "'", "''")
	query := fmt.Sprintf(`
        INSERT INTO Messages (sender, receiver, content, timestamp)
        VALUES ('%s', '%s', '%s', GETDATE())`, from, to, content)
	_, err := execSQLQuery(query)
	return err
}

func ensureLocalDBRunning(instance string) error {
	cmd := exec.Command("sqllocaldb", "i", instance)
	out, err := cmd.CombinedOutput()
	if err != nil || !strings.Contains(string(out), "Running") {
		fmt.Println("⚠️  LocalDB no está activa. Iniciando...")
		startCmd := exec.Command("sqllocaldb", "start", instance)
		startOut, startErr := startCmd.CombinedOutput()
		if startErr != nil {
			return fmt.Errorf("error iniciando LocalDB: %s", string(startOut))
		}
		fmt.Println("✅ LocalDB iniciada correctamente.")
	}
	return nil
}

func main() {
	fmt.Println("⏳ Verificando estado de LocalDB...")

	if err := ensureLocalDBRunning("Local"); err != nil {
		log.Fatalf("❌ No se pudo iniciar LocalDB: %v", err)
	}

	fmt.Println("⏳ Verificando conexión con la base de datos...")
	out, err := execSQLQuery("SELECT GETDATE();")
	if err != nil {
		log.Fatalf("❌ No se pudo conectar a la base de datos: %v\nSalida: %s", err, out)
	} else {
		fmt.Println("✅ Conexión con la base de datos establecida.")
	}

	server := NewServer()
	http.HandleFunc("/ws", server.handleWS)
	fmt.Println("🚀 Servidor de señalización escuchando en http://localhost:8080/ws")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
