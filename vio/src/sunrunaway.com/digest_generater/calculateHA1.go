package main

import (
    http_digest "github.com/SunRunAway/go_httpauth"
    "os"
    "bytes"
    "io"
    "strings"
    "fmt"
)

const (
    realm = "sunrunaway.com"
)

func main() {
    buf := new(bytes.Buffer)
    io.Copy(buf, os.Stdin)
    q := strings.Split(buf.String(), "\n")

    if len(q) < 2 {
        fmt.Println("error!")
        return
    }
    username := q[0]
    password := q[1]

    digest := http_digest.CalculateHA1(username, realm, password)
    fmt.Printf("\n\n\nusername:\n%s\n", username)
	//fmt.Printf("pass:\n%s\n", password)
    fmt.Printf("digest:\n%s\n", digest)
}