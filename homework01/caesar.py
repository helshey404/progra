import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE

    alph_b = []
    c = 65
    r = 65

    for b1 in range(0, 26):
        alph_b.append(chr(c))
        c = c + 1

    for b2 in range(26, 53):
        alph_b.append(chr(r))
        r = r + 1

    alph_l = []
    x = 97
    y = 97
    for b1 in range(0, 26):
        alph_l.append(chr(x))
        x = x + 1

    for b2 in range(26, 53):
        alph_l.append(chr(y))
        y = y + 1

    n = len(plaintext)
    for j in range(0, n):
        if plaintext[j] in alph_b or plaintext[j] in alph_l:
            for b in range(0, 26):
                if plaintext[j] == alph_b[b]:
                    ciphertext += alph_b[b + shift]
                if plaintext[j] == alph_l[b]:
                    ciphertext += alph_l[b + shift]
        else:
            ciphertext += plaintext[j]

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE

    alph_b = []
    c = 65
    r = 65

    for b1 in range(0, 26):
        alph_b.append(chr(c))
        c = c + 1

    for b2 in range(26, 53):
        alph_b.append(chr(r))
        r = r + 1

    alph_l = []
    x = 97
    y = 97
    for b1 in range(0, 26):
        alph_l.append(chr(x))
        x = x + 1

    for b2 in range(26, 53):
        alph_l.append(chr(y))
        y = y + 1

    n = len(ciphertext)
    for j in range(0, n):
        if ciphertext[j] in alph_b or ciphertext[j] in alph_l:
            for b in range(26, 52):
                if ciphertext[j] == alph_b[b]:
                    plaintext += alph_b[b - shift]
                if ciphertext[j] == alph_l[b]:
                    plaintext += alph_l[b - shift]
        else:
            plaintext += ciphertext[j]

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
