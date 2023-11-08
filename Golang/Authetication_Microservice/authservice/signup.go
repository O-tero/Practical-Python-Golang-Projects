package authservice

import (
	"net/http"

	"github.com/shadowshot-x/micro-product-go/authservice/data"
)

// adds the user to the database of users
func SignupHandler(rw http.ResponseWriter, r *http.Request) {
	// extra handling should be done at the server side to prevent malicios attacks
	if _, ok := r.Header["Email"]; !ok {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Email missing"))
		return
	}
	if _, ok := r.Header["Username"]; !ok {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Username missing"))
		return
	}
	if _, ok := r.Header["Passwordhash"]; !ok {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Passwordhash Missing"))
		return
	}
	if _, ok := r.Header["Fullname"]; !ok {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Fullname Missing"))
		return
	}

	// validate and then add the user
	check := data.AddUserObject(r.Header["Email"][0], r.Header["Username"][0], r.Header["Password"][0], r.Header["Fullname"][0], 0)
	// If false means username already exists
	if !check {
		rw.WriteHeader(http.StatusConflict)
		rw.Write([]byte("Email or Username already exists"))
		return
	}
	rw.WriteHeader(http.StatusOK)
	rw.Write([]byte("User Created"))
}
