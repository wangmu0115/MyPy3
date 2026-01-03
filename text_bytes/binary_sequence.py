from array import array

if __name__ == "__main__":
    cafe = bytes("café", encoding="utf-8")
    print(">>>", cafe, cafe[0], cafe[-1:])
    cafe_arr = bytearray(cafe)
    print(">>>", cafe_arr, cafe_arr[0], cafe_arr[-1:])

    print("*" * 80)
    print(">>>", bytes.fromhex("314BCEA9"))

    print("*" * 80)
    numbers = array("h", [-2, -1, 0, 1, 2])
    octets = bytes(numbers)
    print(">>>", numbers, octets)
