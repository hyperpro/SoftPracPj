package cipher

import (
	"bytes"
	"testing"
)

var srcs = [][]byte{
	[]byte("1234567812345678"),
	[]byte("src"),
}

func doTest(c Cipher, t *testing.T) {
	for _, src := range srcs {
		dst := c.Encrypt(src)
		src2, _ := c.Decrypt(dst)
		if !bytes.Equal(src, src2) {
			t.Error(string(src), string(src2))
		}
	}
}

func TestCipher(t *testing.T) {
	c1, err := NewAesCipher([]byte("1234567812345678"))
	if err != nil {
		t.Fatal(err)
	}
	doTest(c1, t)

	c2, err := NewExpandCipher()
	if err != nil {
		t.Fatal(err)
	}
	doTest(c2, t)

	c3, err := NewMixCipher(c1, c2)
	if err != nil {
		t.Fatal(err)
	}
	doTest(c3, t)
}
