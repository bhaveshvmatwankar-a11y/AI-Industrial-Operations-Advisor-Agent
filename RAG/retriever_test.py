from rag_retriever import retrieve_knowledge


question = "Why does a CNC machine have high vibration?"


context = retrieve_knowledge(
    question
)


print("\nRetrieved Knowledge:")
print("=" * 60)
print(context)
