package cipher

type MixCipher struct {
    ciphers []Cipher
}

func NewMixCipher(ciphers... Cipher) (*MixCipher, error) {
    return &MixCipher{ciphers}, nil
}

func (s *MixCipher) Encrypt(src []byte) (dst []byte) {
    for k := 0; k < len(s.ciphers); k++ {
        src = s.ciphers[k].Encrypt(src)
    }
    return src
}

func (s *MixCipher) Decrypt(dst []byte) (src []byte, err error) {
    for k := len(s.ciphers) - 1; k >= 0; k-- {
        dst, err = s.ciphers[k].Decrypt(dst)
        if err != nil {
            return
        }
    }
    return dst, nil
}
