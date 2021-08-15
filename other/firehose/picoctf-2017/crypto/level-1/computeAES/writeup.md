We are given all the required parameters to decrypt the ciphertext using AES in ECB mode.

Using python and PyCrypto to do so we get the flag:
`flag{do_not_let_machines_win_1e6b4cf4}__________`

Simply removing the padding bytes ('\_') we get the flag

Flag: `flag{do_not_let_machines_win_1e6b4cf4}`
