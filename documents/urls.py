from django.urls import path
from .views import (
    upload_document,
    ask_document,
    chat_api,
    document_library,
    chat_history,
    delete_documents,
    logout_view
)

urlpatterns = [

    path(
        "upload/",
        upload_document,
        name="upload_document"
    ),

    path(
        "chat/",
        ask_document,
        name="ask_document"
    ),
    path(
        "chat-api/",
        chat_api,
        name="chat_api"
    ),

    path(
        "library/",
        document_library,
        name="document_library"
    ),

    path(
        "history/",
        chat_history,
        name="chat_history"
    ),
    path(
    "delete/",
    delete_documents,
    name="delete_documents"
),
    path(
        'logout/',
        logout_view,
        name='logout'
    ),

]
