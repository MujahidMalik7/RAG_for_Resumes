from retriever import retrieve
from generator import generate

while True:
    query = input("Query: ")
    if not query.split():
        continue
    elif query in ["exit", "quit", "x", 'bye']:
        print("Goodbye!")
        break
    else:
        results = retrieve(query)
        response = (generate(query, results))
        print ("\n")
        print ("Sources: ")
        for r in results:
            print (f"- {r['source']} (chunk {r['chunk_id']})")
        print ("Answer: ", response)
