package cipher

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"encoding/binary"
	"errors"
)

var (
	EDecrypt = errors.New("Decrypt failed.")
)

// ===================================================================

type AesCipher struct {
	cipher    cipher.Block
	blockSize int
}

func NewAesCipher(secretKey []byte) (*AesCipher, error) {
	c, err := aes.NewCipher(secretKey)
	if err != nil {
		return nil, err
	}
	return &AesCipher{c, c.BlockSize()}, nil
}

func (s *AesCipher) Encrypt(src []byte) (dst []byte) {

	length := len(src)

	if length%s.blockSize != 0 {
		reserved := make([]byte, s.blockSize-length%s.blockSize)
		src = bytes.Join([][]byte{src, reserved}, nil)
	}
	lengthRecord := make([]byte, s.blockSize)
	binary.PutVarint(lengthRecord, int64(length))
	src = bytes.Join([][]byte{src, lengthRecord}, nil)

	dst = make([]byte, len(src))

	for i := 0; i < len(src); i += s.blockSize {
		s.cipher.Encrypt(dst[i:i+s.blockSize], src[i:i+s.blockSize])
	}
	return dst
}

func (s *AesCipher) Decrypt(dst []byte) (src []byte, err error) {
	if len(dst)%s.blockSize != 0 {
		err = EDecrypt
		return
	}

	src = make([]byte, len(dst))

	for i := 0; i < len(dst); i += s.blockSize {
		s.cipher.Decrypt(src[i:i+s.blockSize], dst[i:i+s.blockSize])
	}

	lengthRecord := src[len(src)-16:]
	length, n := binary.Varint(lengthRecord)
	if n <= 0 {
		err = EDecrypt
		return
	}

	src = src[:length]
	return
}
