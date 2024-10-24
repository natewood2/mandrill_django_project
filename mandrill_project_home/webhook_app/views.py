import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import MandrillEvent
from datetime import datetime

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def mandrill_events(request):
    if request.method == 'POST':
        try:
            raw_body = request.body.decode('utf-8')
            print(f"Raw request body: {raw_body}")

            if not raw_body:
                return JsonResponse({'error': 'Empty payload'}, status=400)

            events = json.loads(raw_body)

            for event in events:
                message_id = event.get('msg', {}).get('_id')
                event_type = event.get('event')
                timestamp = datetime.fromtimestamp(event.get('ts', 0))
                payload = event

                MandrillEvent.objects.update_or_create(
                    message_id=message_id,
                    defaults={
                        'event_type': event_type,
                        'timestamp': timestamp,
                        'payload': payload,
                    }
                )

                if event_type == 'open':
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        'mandrill_events',
                        {
                            'type': 'email.opened',
                            'message': {
                                'message_id': message_id,
                                'event': 'open',
                                'ts': event.get('ts'),
                            },
                        }
                    )

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
