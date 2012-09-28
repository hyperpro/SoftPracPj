package cipher


type Cipher interface {
    Encrypt(src []byte) (dst []byte)
    Decrypt(dst []byte) (src []byte, err error)
}
