import csv_input
import fetcher


def main() -> None:
    items_to_find = csv_input.read_csv("../files/example_input.csv")
    for sku, ingredients in items_to_find.items():
        print("checking", sku)
        for ingr in ingredients:
            findings = fetcher.search(ingr)
            if ingr in findings:
                print("Found exact match:", ingr)
            else:
                print("Trying to find partial match...")
                match = []
                for item in findings:
                    if ingr in item:
                        match.append(item)
                if match:
                    print("Partial match:", ingr, match)


if __name__ == "__main__":
    main()
