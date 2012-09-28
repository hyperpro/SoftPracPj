package main

import (
	http_digest "bitbucket.org/taruti/http_digest"
	"net/http"
)

var s = http_digest.NewDigest("MyRealm", func(user, realm string) string {
	return http_digest.CalculateHA1(user, realm, "mypass")
})

func rootHandler(w http.ResponseWriter, r *http.Request) {
	if !s.Auth(w, r) {
		return
	}
	w.Write([]byte("<html><title>Hello</title><h1>Hello</h1></html>"))
}

func main() {
	http.HandleFunc("/", rootHandler)
	http.ListenAndServe(":8080", nil)
}
