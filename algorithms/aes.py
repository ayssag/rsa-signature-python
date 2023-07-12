# def aesEncryption(plaintext, key):
#     _remaining_counter = []
#     while len(_remaining_counter) < len(plaintext):
#         _remaining_counter += _aes.encrypt(_counter.value)
#         _counter.increment()

#     plaintext = _string_to_bytes(plaintext)

#     encrypted = [ (p ^ c) for (p, c) in zip(plaintext, _remaining_counter) ]
#     _remaining_counter = _remaining_counter[len(encrypted):]

#     return _bytes_to_string(encrypted)