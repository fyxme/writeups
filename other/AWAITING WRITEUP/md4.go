package main

import (
    "golang.org/x/crypto/md4"
    "fmt"
    //"strconv"
    "unsafe"
    "encoding/hex"
    "unicode"
)

func unsafeEqual(a string, b []byte) bool {
    bbp := *(*string)(unsafe.Pointer(&b))
    return a == bbp
}

func onlyDigits(bs []byte) bool {
    bss := hex.EncodeToString(bs[1:])
    for _, b := range bss {
        if unicode.IsLetter(b) {
            return false
        }
    }
    return true
}

func main() {
    s := "0e"

    comp, err := hex.DecodeString(s)
    if err != nil {
        panic(err)
    }

    for i:=0;i<10000000000;i++ {
        // The pattern for generating a hash is `sha1.New()`,
        // `sha1.Write(bytes)`, then `sha1.Sum([]byte{})`.
        // Here we start with a new hash.
        h := md4.New()
        // `Write` expects bytes. If you have a string `s`,
        // use `[]byte(s)` to coerce it to bytes.
        h.Write([]byte(fmt.Sprintf("0e%d",i)))

        // This gets the finalized hash result as a byte
        // slice. The argument to `Sum` can be used to append
        // to an existing byte slice: it usually isn't needed.
        bs := h.Sum(nil)

        if comp[0] == bs[0] && onlyDigits(bs) {

            // SHA1 values are often printed in hex, for example
            // in git commits. Use the `%x` format verb to convert
            // a hash results to a hex string.
            fmt.Printf("0e%d %x\n", i, bs)
        }
    }
}
