from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def get_mock_products():
    products = [
        {
            "id": "prod-1",
            "name": "Coca-Cola 600ml",
            "typeId": "compliant",
            "imageUrl": "https://images.pexels.com/photos/8754654/pexels-photo-8754654.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": True,
            "position": { "x": 1, "y": 2, "z": 1 },
            "expectedPosition": { "x": 1, "y": 2, "z": 1 }
        },
        {
            "id": "prod-2",
            "name": "Pepsi 600ml",
            "typeId": "partial",
            "imageUrl": "https://images.pexels.com/photos/17708640/pexels-photo-17708640/free-photo-of-food-drink-pepsi-cola.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": { "x": 1, "y": 3, "z": 1 },
            "expectedPosition": { "x": 1, "y": 4, "z": 1 }
        },
        {
            "id": "prod-3",
            "name": "Sprite 600ml",
            "typeId": "compliant",
            "imageUrl": "https://images.pexels.com/photos/6103231/pexels-photo-6103231.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": True,
            "position": { "x": 2, "y": 2, "z": 1 },
            "expectedPosition": { "x": 2, "y": 2, "z": 1 }
        },
        # ... (agrega aquí el resto de tus productos mock del frontend) ...
    ]
    return {
        "metrics": {},
        "compliance_counts": {},
        "products": products,
        "positions": [],
        "analyzed_image_url": "",
        "detection_boxes": []
    }

def planograma_analisis(request):
    logger.info('GET /api/planograma/analisis/ called')
    return JsonResponse(get_mock_products())

@csrf_exempt
def planograma_analizar_imagen(request):
    if request.method == 'POST':
        logger.info('POST /api/planograma/analizar-imagen/ called')
        return JsonResponse(get_mock_products())
    return JsonResponse({'error': 'Método no permitido'}, status=405)
