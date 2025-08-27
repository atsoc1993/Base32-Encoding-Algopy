from algopy import ARC4Contract, arc4, op, Txn, urange, UInt64, String, itxn, ensure_budget, OpUpFeeSource
from algopy.arc4 import abimethod, DynamicBytes, Byte


class SenderToUtf8(ARC4Contract):
    def __init__(self) -> None:
        pass

    @abimethod
    def base32_sender_address(self) -> None:
        ALPHABET = String("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567").bytes
        pk = Txn.sender.bytes

        h = op.sha512_256(pk)
        cksum = h[28:32]

        raw = DynamicBytes()
        raw.extend(DynamicBytes(pk))
        raw.extend(DynamicBytes(cksum))

        data = raw.native
        bits = UInt64(0)
        bitlen = UInt64(0)
        out = DynamicBytes()


        for i in urange(data.length):
            ensure_budget(required_budget=700, fee_source=OpUpFeeSource.GroupCredit)

            b = arc4.UInt64.from_bytes(data[i]).native
            bits = (bits << UInt64(8)) | b
            bitlen += UInt64(8)

            while bitlen >= UInt64(5):
                bitlen -= UInt64(5)
                idx = (bits >> bitlen) & UInt64(0b11111)
                ch = ALPHABET[idx]
                out.append(Byte(arc4.UInt64.from_bytes(ch).native))

        if bitlen > UInt64(0):
            idx = (bits << (UInt64(5) - bitlen)) & UInt64(0b11111)
            ch = ALPHABET[idx]
            out.append(Byte(arc4.UInt64.from_bytes(ch).native))

        addr_str = String.from_bytes(out.native)

        itxn.Payment(
            amount=0,
            receiver=Txn.sender,
            note=addr_str
        ).submit()
