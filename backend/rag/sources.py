import os

def extract_sources(documents):

    sources = []

    seen = set()


    for doc in documents:

        source = (
            doc.metadata.get(
                "source",
                "unknown"
            ),

            doc.metadata.get(
                "page",
                "unknown"
            )
        )


        if source not in seen:

            seen.add(source)

            sources.append(
                {
                    "document": os.path.basename(source[0]),
                    "page": source[1]
                }
            )


    return sources