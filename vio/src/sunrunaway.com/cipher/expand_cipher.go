package cipher

import (
	"math/rand"
	"time"
)

type ExpandCipher struct {
}

func NewExpandCipher() (*ExpandCipher, error) {
	rand.Seed(time.Now().UnixNano())
	return &ExpandCipher{}, nil
}

func (s *ExpandCipher) Encrypt(src []byte) (dst []byte) {
	dst = make([]byte, len(src)*2)
	for k, v := range src {
		dst[2*k] = v
		dst[2*k+1] = byte(rand.Int())
	}
	return
}

func (s *ExpandCipher) Decrypt(dst []byte) (src []byte, err error) {
	src = make([]byte, len(dst)/2)
	for i := 0; i < len(dst); i += 2 {
		src[i/2] = dst[i]
	}
	return
}
