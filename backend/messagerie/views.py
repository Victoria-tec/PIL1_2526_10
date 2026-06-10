from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Conversation, Message
import json


def liste_conversations(request):
    if not request.user.is_authenticated:
        return render(request, 'chat.html', {'conversations': []})
    conversations = request.user.conversations.all().order_by('-creee_le')
    return render(request, 'chat.html', {
        'conversations': conversations
    })


def detail_conversation(request, conversation_id):
    if not request.user.is_authenticated:
        return render(request, 'chat.html', {'conversations': []})
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    conversations = request.user.conversations.all().order_by('-creee_le')
    return render(request, 'chat.html', {
        'conversations': conversations,
        'conversation_active': conversation,
    })


def envoyer_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        data = json.loads(request.body)
        contenu = data.get('contenu', '').strip()
        if contenu:
            message = Message.objects.create(
                conversation=conversation,
                expediteur=request.user,
                contenu=contenu
            )
            return JsonResponse({
                'status': 'ok',
                'message_id': message.id,
                'expediteur': request.user.get_full_name() or request.user.username,
                'contenu': message.contenu,
                'envoye_le': message.envoye_le.strftime('%H:%M'),
            })
    return JsonResponse({'status': 'erreur'}, status=400)
