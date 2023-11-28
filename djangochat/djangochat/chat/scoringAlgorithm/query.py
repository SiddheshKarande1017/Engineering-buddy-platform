from .invdx import build_data_structures
from .rank import score_BM25
from .cosine import cosine_score
import operator


class QueryProcessor:
	def __init__(self, queries, corpus):
		self.queries = queries
		self.index, self.dlt = build_data_structures(corpus)
		self.corpus=corpus

	def run(self):
		results = []
		for query in self.queries:
			results.append(self.run_query(query))
		return results

	def run_query(self, query):
		query_result = dict()
		for term in query:
			if term in self.index:
				doc_dict = self.index[term] # retrieve index entry
				for docid, freq in doc_dict.items(): #for each document and its word frequency
					score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
									   dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length() ) # calculate score
					# score2=cosine_score(self.corpus[docid], self.queries[0])
					# print(score2)
					# print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + docid)
					# print(self.corpus[docid])
					# print("\n\n\n\n\n\n\n\n")
					# print(self.queries[0])
					# print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
					if docid in query_result: #this document has already been scored once
						query_result[docid] += (score)
					else:
						query_result[docid] = score
		for docid in query_result:
			score2 = cosine_score(self.corpus[docid], self.queries[0])
			query_result[docid] += (score2)

		return query_result
