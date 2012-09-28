package vio

import (
	"crypto/sha1"
	"encoding/base64"
	"io"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"sunrunaway.com/keystore"
	"sunrunaway.com/store"
	"time"
)

func randomBytes(length int) []byte {
	r := length
	j := 0

	b := make([]byte, r)
	for i := 0; i < r; i++ {
		//j = (j + 1) % 10
		j = rand.Intn(10)
		b[i] = byte(j) + byte('0')
	}
	return b
}

// ===================================================================================

type Service struct {
	stg           *store.Store
	myhost        string
	urlExpireTime int64
}

func New(stg *store.Store, myhost string, urlExpireTime int64) (s *Service) {
	return &Service{stg, myhost, urlExpireTime}
}

// ===============================================================================

//
// GET /get-thumb/<key>
//
func (s *Service) getThumb(w http.ResponseWriter, key string) {
	r, length, err := s.stg.GetThumb(key)
	if err != nil {
		log.Println("getThumb: s.stg.Get error:", err)
		w.WriteHeader(404)
		return
	}
	defer r.Close()

	h := w.Header()
	h.Set("Content-Length", strconv.FormatInt(length, 10))
	w.WriteHeader(200)
	io.CopyN(w, r, length)
}

//
// GET /file/<encodedKeyHandle>(?thumb=1)
//
func (s *Service) file(w http.ResponseWriter, req *http.Request) {
	query := strings.Split(req.URL.Path[1:], "/")
	if len(query) < 2 {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	encodedKeyHandle := query[1]
	kh, err := keystore.Decode(encodedKeyHandle)
	if err != nil {
		log.Println("file: keystore.Decode error:", err)
		w.WriteHeader(404)
		return
	}
	key := kh.Key
	if time.Now().Unix() > kh.Expire {
		log.Println("file: encodedKeyHandle expired.")
		w.WriteHeader(404)
		return
	}
	log.Println("file: key:", key)


	if q := req.URL.Query(); q.Get("thumb") == "1" {
		s.getThumb(w, key)
		return
	}

	r, length, err := s.stg.Get(key)
	if err != nil {
		log.Println("file: s.stg.Get error:", err)
		w.WriteHeader(404)
		return
	}
	defer r.Close()

	h := w.Header()

	h.Set("Accept-Ranges", "bytes")
	h.Set("Content-Transfer-Encoding", "binary")

	if rg1, ok := req.Header["Range"]; ok {
		from, to, ok := ParseOneRange(rg1[0], length)
		if !ok {
			log.Println("get: ParseOnerange !ok")
			w.WriteHeader(http.StatusRequestedRangeNotSatisfiable)
			return
		}
		rg := "bytes " + strconv.FormatInt(from, 10) + "-" + strconv.FormatInt(to-1, 10) + "/" + strconv.FormatInt(length, 10)
		h.Set("Content-Length", strconv.FormatInt(to-from, 10))
		h.Set("Content-Range", rg)
		w.WriteHeader(206)
		r.Seek(from, 0)
		io.Copy(w, io.LimitReader(r, to-from))
	} else {
		h.Set("Content-Length", strconv.FormatInt(length, 10))
		w.WriteHeader(200)
		io.CopyN(w, r, length)
	}
}

// ---------------------------------------------------------------------------

//
// GET /get/<key>
// return: get-url
//
func (s *Service) get(w http.ResponseWriter, req *http.Request) {
	query := strings.Split(req.URL.Path[1:], "/")
	if len(query) < 2 {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	key := query[1]
	log.Println("get: key:", key)

	isExist := s.stg.Check(key)
	if !isExist {
		log.Println("get: do not exist")
		w.WriteHeader(404)
		return
	}

	kh := keystore.KeyStore{
		Key:    key,
		Expire: time.Now().Unix() + s.urlExpireTime,
	}
	encodedKeyHandle := keystore.Encode(kh)
	url := s.myhost + "/file/" + encodedKeyHandle
	w.Header().Set("Content-Length", strconv.Itoa(len(url)))
	w.WriteHeader(200)
	io.WriteString(w, url)
}

// ---------------------------------------------------------------------------

func generateKey() string {
	h := sha1.New()
	h.Write([]byte(time.Now().String()))
	h.Write(randomBytes(20))
	name := base64.URLEncoding.EncodeToString(h.Sum(nil))
	return name
}

//
// POST /upload/<encodedKeyHandle>
// BODY: video stream with Content-Length
// return: <key>
//
func (s *Service) upload(w http.ResponseWriter, req *http.Request) {
	query := strings.Split(req.URL.Path[1:], "/")
	if len(query) < 2 {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	encodedKeyHandle := query[1]
	kh, err := keystore.Decode(encodedKeyHandle)
	if err != nil {
		log.Println("upload: keystore.Decode error:", err)
		w.WriteHeader(404)
		return
	}
	key := kh.Key
	if time.Now().Unix() > kh.Expire {
		log.Println("upload: encodedKeyHandle expired.")
		w.WriteHeader(404)
		return
	}
	log.Println("upload: key:", key)

	defer req.Body.Close()
	err = s.stg.Put(key, req.Body, req.ContentLength)
	if err != nil {
		log.Println("upload: s.stg.Put", err)
		w.WriteHeader(400)
		return
	}
	w.Header().Set("Content-Length", strconv.Itoa(len(key)))
	w.WriteHeader(200)
	io.WriteString(w, key)
}

//
// GET /put-auth
// return: put-url
//
func (s *Service) putAuth(w http.ResponseWriter, req *http.Request) {
	key := generateKey()
	log.Println("putAuth: key:", key)

	kh := keystore.KeyStore{
		Key:    key,
		Expire: time.Now().Unix() + s.urlExpireTime,
	}
	encodedKeyHandle := keystore.Encode(kh)
	url := s.myhost + "/upload/" + encodedKeyHandle
	w.Header().Set("Content-Length", strconv.Itoa(len(url)))
	w.WriteHeader(200)
	io.WriteString(w, url)
}

// ---------------------------------------------------------------------------

//
// GET /delete/<key>
//
func (s *Service) delete(w http.ResponseWriter, req *http.Request) {
	query := strings.Split(req.URL.Path[1:], "/")
	if len(query) < 2 {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	key := query[1]

	err := s.stg.Delete(key)
	if err != nil {
		log.Println("delete: s.stg.Delete error", err)
		w.WriteHeader(404)
		return
	}
	w.WriteHeader(200)
}

// ===============================================================================

func (s *Service) RegesterHandlers(mux *http.ServeMux) error {
	mux.HandleFunc("/file/", func(w http.ResponseWriter, req *http.Request) {
		s.file(w, req)
	})
	mux.HandleFunc("/get/", func(w http.ResponseWriter, req *http.Request) {
		s.get(w, req)
	})

	mux.HandleFunc("/upload/", func(w http.ResponseWriter, req *http.Request) {
		s.upload(w, req)
	})
	mux.HandleFunc("/put-auth", func(w http.ResponseWriter, req *http.Request) {
		s.putAuth(w, req)
	})

	mux.HandleFunc("/delete/", func(w http.ResponseWriter, req *http.Request) {
		s.delete(w, req)
	})
	return nil
}

func (s *Service) Run(addr string) error {
	mux := http.NewServeMux()
	err := s.RegesterHandlers(mux)
	if err != nil {
		return err
	}
	return http.ListenAndServe(addr, mux)
}
