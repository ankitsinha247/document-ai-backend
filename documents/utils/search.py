from pgvector.django import CosineDistance
from documents.models import DocumentChunk


def search_chunks(query_embedding, document_id=None, limit=10):

    queryset = DocumentChunk.objects.all()

    if document_id:
        queryset = queryset.filter(
            document_id=document_id
        )

    results = queryset.annotate(
        distance=CosineDistance(
            "embedding",
            query_embedding
        )
    ).order_by("distance")[:limit]

    return results