from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from openai import OpenAI

from .models import ChatMessage

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_view(request):
    user = request.user
    message = request.data.get("message")

    if not message:
        return Response({"detail": "Message required"}, status=400)

    # user message save
    ChatMessage.objects.create(
        user=user,
        message=message,
        is_bot=False
    )

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=message
        )

        reply = response.output_text

    except Exception as e:
        return Response({"detail": str(e)}, status=500)

    # bot reply save
    ChatMessage.objects.create(
        user=user,
        message=reply,
        is_bot=True
    )

    return Response({
        "reply": reply
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history_view(request):
    user = request.user

    chats = ChatMessage.objects.filter(user=user).order_by('-created_at')[:20]

    data = []
    for chat in chats:
        data.append({
            "message": chat.message,
            "is_bot": chat.is_bot,
            "time": chat.created_at
        })

    return Response({
        "chats": data
    })