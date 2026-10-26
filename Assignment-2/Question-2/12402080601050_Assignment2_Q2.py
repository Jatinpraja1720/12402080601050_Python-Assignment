from html.parser import HTMLParser
import re

# Extract products from HTML
class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []

        self.depth = 0
        self.card_depth = None
        self.field = None
        self.field_depth = None
        self.card = None

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        attrs = dict(attrs)
        classes = attrs.get("class", "").lower().split()

        # Start a new product card
        if self.card is None and (
            "product" in classes or "product-card" in classes
        ):
            self.card = {"name": "", "price": "", "rating": ""}
            self.card_depth = self.depth

        if self.card is not None and self.field is None:
            if any(c in classes for c in ["name", "product-name"]):
                self.field = "name"
                self.field_depth = self.depth

            elif any(c in classes for c in ["price", "product-price"]):
                self.field = "price"
                self.field_depth = self.depth

            elif any(c in classes for c in ["rating", "product-rating"]):
                self.field = "rating"
                self.field_depth = self.depth

    def handle_data(self, data):
        if self.card is not None and self.field is not None:
            self.card[self.field] += data

    def handle_endtag(self, tag):
        # Finish reading a product field
        if self.field is not None and self.depth == self.field_depth:
            self.field = None
            self.field_depth = None

        # Finish reading a product card
        if self.card is not None and self.depth == self.card_depth:
            if all(self.card[x].strip() for x in
                   ["name", "price", "rating"]):
                self.products.append(self.card)

            self.card = None
            self.card_depth = None
            self.field = None
            self.field_depth = None

        self.depth -= 1


# Convert price text into a number
def normalize_price(price_text):
    price_text = price_text.replace(",", "")
    match = re.search(r"\d+(?:\.\d+)?", price_text)

    if match is None:
        return None

    return float(match.group())


# Read one HTML file in small chunks
def read_products(file_path):
    parser = ProductParser()

    with open(file_path, "r", encoding="utf-8",
              errors="ignore") as file:
        while True:
            chunk = file.read(65536)

            if not chunk:
                break

            parser.feed(chunk)

    parser.close()
    return parser.products


def main():
    try:
        first_line = input("Enter p and k: ").split()

        if len(first_line) != 2:
            print("Error: Enter two integers: p and k.")
            return

        p, k = map(int, first_line)

        if not (1 <= p <= 5000 and 1 <= k <= 1000):
            print("Error: p or k is outside the allowed range.")
            return

        file_paths = []

        for i in range(p):
            path = input(f"Enter HTML file {i + 1}: ").strip()

            if not path:
                print("Error: File path cannot be empty.")
                return

            file_paths.append(path)

        # Store one product per unique name
        unique_products = {}

        for path in file_paths:
            for product in read_products(path):
                name = " ".join(product["name"].split())
                price = normalize_price(product["price"])

                try:
                    rating_text = product["rating"].strip()
                    rating_match = re.search(
                        r"\d+(?:\.\d+)?", rating_text
                    )

                    if rating_match is None or price is None:
                        continue

                    rating = float(rating_match.group())

                    # Ignore invalid product information
                    if not name or price < 0 or not (0 <= rating <= 5):
                        continue

                except ValueError:
                    continue

                item = {
                    "name": name,
                    "price": price,
                    "rating": rating
                }

                key = name.casefold()

                # Keep the better-ranked duplicate
                if key not in unique_products:
                    unique_products[key] = item
                else:
                    old = unique_products[key]

                    if (-rating, price, name) < (
                        -old["rating"], old["price"], old["name"]
                    ):
                        unique_products[key] = item

        # Highest rating, then lowest price, then name
        products = sorted(
            unique_products.values(),
            key=lambda x: (-x["rating"], x["price"], x["name"])
        )

        # Print only the top K products
        for item in products[:k]:
            price = item["price"]

            if price.is_integer():
                price = int(price)

            print(item["name"], price, item["rating"])

    except (OSError, UnicodeError) as error:
        print("Error reading file:", error)

    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
