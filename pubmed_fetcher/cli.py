import argparse
import csv
from pubmed_fetcher.fetch import fetch_pubmed_ids, fetch_paper_details

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results as CSV")
    args = parser.parse_args()

    pubmed_ids = fetch_pubmed_ids(args.query)
    results = [fetch_paper_details(pid) for pid in pubmed_ids]

    if args.file:
        save_to_csv(results, args.file)
        print(f"Results saved to {args.file}")
    else:
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
