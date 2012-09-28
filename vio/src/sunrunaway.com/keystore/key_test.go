package keystore

import (
    "testing"
)

var khs = []KeyStore{
    {"key123", 1},
    {"keyabc", 5},
}
func TestEncodeDecode(t *testing.T) {
    for _, kh := range khs {
        ekh := Encode(kh)
        kh2, err := Decode(ekh)
        if err != nil {
            t.Error(err)
        }
        if kh != kh2 {
            t.Error(kh, kh2)
        }
    }
}
