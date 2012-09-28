package keystore

import (
	"encoding/base64"
	"errors"
	"log"
	"strconv"
	"strings"
	"sunrunaway.com/cipher"
)

const (
	// python: os.urandom(string_length)
	salt = "\xdd\xf2\t\xcf\xdb\xdb\xf0d\x80\xd0b\xd3c\x8d\x1c$N\xf1\x98\xc4"
)

var (
	EDecode = errors.New("Decode Key failed.")
)

var g_cipher cipher.Cipher

func init() {
	c1, err := cipher.NewExpandCipher()
	if err != nil {
		log.Fatal(err)
	}
	c2, err := cipher.NewAesCipher()
	if err != nil {
		log.Fatal(err)
	}
	g_cipher, err = cipher.NewMixCipher(c1, c2)
	if err != nil {
		log.Fatal(err)
	}
}

// =======================================================================

type KeyStore struct {
	Key    string
	Expire int64
}

// =======================================================================

func encode(kh KeyStore) (dst []byte) {
	src := []byte(kh.Key + salt + strconv.FormatInt(kh.Expire, 36))
	dst = g_cipher.Encrypt(src)
	log.Println("dst:", dst)
	return
}

func decode(dst []byte) (kh KeyStore, err error) {
	src, err := g_cipher.Decrypt(dst)
	if err != nil {
		return
	}

	q := strings.Split(string(src), salt)
	if len(q) != 2 {
		err = EDecode
		return
	}
	key := q[0]
	expire, err := strconv.ParseInt(q[1], 36, 64)
	if err != nil {
		err = EDecode
		return
	}
	return KeyStore{key, expire}, nil

}

func Encode(kh KeyStore) (encodedKeyHandle string) {
	dst := encode(kh)
	return base64.URLEncoding.EncodeToString(dst)
}

func Decode(encodedKeyHandle string) (kh KeyStore, err error) {
	dst, err := base64.URLEncoding.DecodeString(encodedKeyHandle)
	if err != nil {
		err = EDecode
		return
	}
	kh, err = decode(dst)
	return
}
