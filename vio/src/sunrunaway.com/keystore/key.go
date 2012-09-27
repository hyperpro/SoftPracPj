package keystore

import (
    "encoding/base64"
    "strconv"
    "strings"
    "errors"
)

const (
    salt = "sunrunaway.com"
)

var (
    EDecode = errors.New("Decode Key failed")
)

type KeyStore struct {
    Key string
    Expire int64
}

func EncodeKey(kh KeyStore) (encodedKey string) {
    src := kh.Key + salt + strconv.FormatInt(kh.Expire, 36)
    return base64.URLEncoding.EncodeToString([]byte(src))
}

func DecodeKey(encodedKey string) (kh KeyStore, err error) {
    o, err := base64.URLEncoding.DecodeString(encodedKey)
    if err != nil {
        err = EDecode
        return
    }
    q := strings.Split(string(o), salt)
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