from tmp.bulkfood_v2 import LineItem

if __name__ == "__main__":
    raisins = LineItem("Golden raisins", 10, 6.95)
    print(raisins.subtotal())
    raisins.weight = -20
    print(raisins.subtotal())
