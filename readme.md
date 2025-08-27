## Problem

I have seen many situations where someone asks how to include an address in a note field in such a way that it does not come out as absolute gibberish.

There is no .to_string() for an Account or Address type, and attempting to send the address as bytes (Account.bytes or Address.bytes) via note field still results in gibberish.

## Solution 
Since there are no available base32 encode/decode opcodes, the solution is to calculate the utf-8 encoded string representation manually.

- calculate the checksum from address bytes by hashing it and retrieving the last 4 resulting bytes
- extend the original public key bytes with this checksum
- iterate over these bytes using general base32 encoding logic
- ta-da, include in note fields as needed, the address' will be in a readable and usable format

## Fin
The hard part (which I have done for us) was converting the existing open-source Python implementations of base32 encoding to be algokit-acceptable and type-inferenced for compilation.

Please feel free to use/test this when needed and share if you hear anyone mention "including addresses in note fields"
