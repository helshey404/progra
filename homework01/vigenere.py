def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""

    word = keyword
    while len(word) < len(plaintext):
        word += keyword

    word = word.upper()

    for i in range(len(plaintext)):
        letter = plaintext[i]

        if not letter.isalpha():
            ciphertext += letter
            continue

        low = False
        if letter.islower():
            letter = letter.upper()
            low = True

        code = word[i]

        out = ord(letter) + (ord(code) - ord('A'))

        if out > ord('Z'):
            out = chr(ord('A') + out - ord('Z') - 1)
        else:
            out = chr(out)

        if low:
            out = out.lower()

        ciphertext += out

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""

    word = keyword
    while len(word) < len(ciphertext):
        word += keyword

    word = word.upper()

    for i in range(len(plaintext)):
        letter = plaintext[i]

        if not letter.isalpha():
            plaintext += letter
            continue

        low = False
        if letter.islower():
            letter = letter.upper()
            low = True

        code = word[i]

        out = ord(letter) - (ord(code) - ord('A'))

        if out < ord('A'):
            out = chr(ord('Z') - (ord('A') - out) + 1)
        else:
            out = chr(out)

        if low:
            out = out.lower()

        ciphertext += out

    return plaintext
