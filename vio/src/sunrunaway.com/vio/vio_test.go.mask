package vio

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sunrunaway.com/store"
	"testing"
	"time"

	"bytes"
)

const root = "testFolder"
const testfile = "123.png"

func Test(t *testing.T) {
	os.Mkdir(root, 0755)
	stg := store.NewStore(root)
	service := New(stg, "http://localhost:12333", 3600)
	go service.Run(":12333")
	time.Sleep(1e9)

	defer os.RemoveAll(root)

	src, err := os.Open(testfile)
	if err != nil {
		t.Fatal(err)
	}
	defer src.Close()
	fi, err := os.Stat(testfile)
	if err != nil {
		t.Fatal(err)
	}
	fsize := fi.Size()

	resp, err := http.Get("http://localhost:12333/put-auth")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	buf := new(bytes.Buffer)
	io.CopyN(buf, resp.Body, resp.ContentLength)
	putUrl := buf.String()

	req, err := http.NewRequest("POST", putUrl, src)
	if err != nil {
		t.Fatal(err)
	}
	req.ContentLength = fsize
	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	name := new(bytes.Buffer)
	io.Copy(name, resp.Body)
	fmt.Println(name.String(), "\n")

	resp, err = http.Get("http://localhost:12333/get/" + name.String())
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	b := new(bytes.Buffer)
	io.CopyN(b, resp.Body, resp.ContentLength)
	getUrl := b.String()

	resp, err = http.Get(getUrl)
	if err != nil {
		t.Fatal(err)
	}
	if resp.ContentLength != fsize {
		t.Error(fsize, resp.ContentLength)
	}
}
