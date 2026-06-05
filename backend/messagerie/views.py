from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message
import json

@login_required
def liste_conversations(request):
    conversations = request.user.conversations.all().order_by('-creee_le')
    return render(request, 'messagerie/liste_conversations.html', {
        'conversations': conversations
    })

@login_required
def detail_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all().order_by('envoye_le')
    return render(request, 'messagerie/detail_conversation.html', {
        'conversation': conversation,
        'messages': messages
    })

@login_required
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
                'expediteur': request.user.username,
                'contenu': message.contenu,
                'envoye_le': message.envoye_le.strftime('%H:%M')
            })
    return JsonResponse({'status': 'erreur'}, status=400)
# Create your views here.
