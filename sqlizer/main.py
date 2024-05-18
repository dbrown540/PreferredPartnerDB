import time
from .scripts.document_parser import DocumentParser

def main():
    start = time.time()
    doc_parser = DocumentParser()
    doc_parser.parse_document("C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//files//sample-job-description.pdf")
    end = time.time()
    print("Execution time: ", end - start)

if __name__ == "__main__":
    main()