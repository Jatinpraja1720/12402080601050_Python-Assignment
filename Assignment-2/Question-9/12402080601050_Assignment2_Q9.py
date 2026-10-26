
class Product:
    def __init__(self, pid, name, stock, purchase, selling):
        self.pid = pid
        self.name = name
        self.stock = stock
        self.purchase = purchase
        self.selling = selling


class Inventory:
    def __init__(self):
        self.products = {}

    def add(self, p):
        self.products[p.pid] = p
        print("Product added")

    def delete(self, pid):
        if pid in self.products:
            del self.products[pid]
            print("Product deleted")
        else:
            print("Product not found")

    def update(self, pid, stock):
        if pid in self.products:
            self.products[pid].stock = stock
            print("Stock updated")
        else:
            print("Product not found")

    def total_value(self):
        return sum(p.stock * p.purchase
                   for p in self.products.values())

    def __add__(self, other):
        result = Inventory()
        result.products = self.products.copy()

        for pid, p in other.products.items():
            if pid in result.products:
                old = result.products[pid]
                old.stock += p.stock
                old.purchase = min(old.purchase, p.purchase)
                old.selling = max(old.selling, p.selling)
            else:
                result.products[pid] = Product(
                    p.pid, p.name, p.stock,
                    p.purchase, p.selling
                )
        return result

    def __lt__(self, other):
        return self.total_value() < other.total_value()

    def display(self):
        for p in sorted(self.products.values(),
                        key=lambda x: x.pid):
            print(f"{p.pid} {p.name} stock={p.stock} "
                  f"purchase={p.purchase} selling={p.selling}")
        print("Total valuation:", self.total_value())


# Create inventories
A = Inventory()
B = Inventory()

A.add(Product("P1", "Pen", 10, 5, 8))
B.add(Product("P1", "Pen", 7, 4, 9))

# Merge inventories using operator overloading
C = A + B

print("\nMerged Inventory:")
C.display()

# Compare inventories
if A < B:
    print("Inventory A has lower value")
elif B < A:
    print("Inventory B has lower value")
else:
    print("Both inventories have equal value")

# Update and delete examples
C.update("P1", 20)
C.delete("P1")
