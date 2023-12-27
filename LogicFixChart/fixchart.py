import pandas as pd
import re
from rank_bm25 import BM25Okapi


df = pd.read_csv("./Current_Employee_Names__Salaries__and_Position_Titles_-_Full-time.csv")
viz_code = pd.read_csv("./sample_data_hepha (4).csv")

column_name = df.columns

input_string = viz_code['code_viz'][39]

matches = re.findall(r'(?<!title=)(?:"([^"]*)"|\'([^\']*)\')', input_string)

# Extract individual words without duplicates using a set
name_column_viz = {match[0] if match[0] else match[1] for match in matches}

# Convert the set to a list if needed
name_column_viz_list = list(name_column_viz)

print(name_column_viz_list)

for query in name_column_viz:
    # Tokenize your documents (you may need more advanced tokenization based on your needs)
    tokenized_corpus = [document.lower().split() for document in column_name]

    # Create BM25 model
    bm25 = BM25Okapi(tokenized_corpus)

    # Query
    tokenized_query = query.lower().split()

    # Get document scores for the query
    doc_scores = bm25.get_scores(tokenized_query)

    doc_score_pairs = list(zip(column_name, doc_scores))

    # Sort documents by score
    sorted_docs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    if sorted_docs:
        document, score = sorted_docs[0]
        if score >= 1.0:
            print(f"Query: {query}")

            print(f"Top 1 Document: {document}, {score}")

            input_string = re.sub(fr'"{re.escape(query)}"|\'{re.escape(query)}\'', f'"{document}"', input_string)

            print(input_string)
        
try:
    exec(input_string)
    chart_fig = plot_chart(df)
    chart_fig.show()
except Exception as e:
    print(f"Error: {e}")

