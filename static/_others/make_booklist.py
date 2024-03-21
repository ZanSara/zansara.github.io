import csv

books = []
raw_books = []
with open('ol_books.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[6] == "Already Read":
            # url, title, author
            books.append((f"https://openlibrary.org/works/{row[0]}", row[1], row[2]))

books.sort(key=lambda row: row[2])

result = []
for row in books:
    result.append(f"- [_\"{row[1]}\"_]({row[0]}), by {row[2]}\n")

list = "".join(result)
print(list)