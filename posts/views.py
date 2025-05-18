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
            "typeId": "found",
            "imageUrl": "https://images.pexels.com/photos/8754654/pexels-photo-8754654.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": True,
            "position": {"x": 1, "y": 2, "z": 1},
            "expectedPosition": {"x": 1, "y": 2, "z": 1}
        },
        {
            "id": "prod-2",
            "name": "Pepsi 600ml",
            "typeId": "misplaced",
            "imageUrl": "https://images.pexels.com/photos/17708640/pexels-photo-17708640/free-photo-of-food-drink-pepsi-cola.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 1, "y": 3, "z": 1},
            "expectedPosition": {"x": 1, "y": 4, "z": 1}
        },
        {
            "id": "prod-3",
            "name": "Sprite 600ml",
            "typeId": "missing",
            "imageUrl": "https://images.pexels.com/photos/6103231/pexels-photo-6103231.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 0, "y": 0, "z": 0},
            "expectedPosition": {"x": 2, "y": 2, "z": 1}
        },
        {
            "id": "prod-4",
            "name": "Fanta 600ml",
            "typeId": "non-compliant",
            "imageUrl": "https://images.pexels.com/photos/11399218/pexels-photo-11399218.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 2, "y": 3, "z": 1},
            "expectedPosition": {"x": 2, "y": 4, "z": 1}
        },
        {
            "id": "prod-5",
            "name": "Doritos Nacho",
            "typeId": "compliant",
            "imageUrl": "https://images.pexels.com/photos/7198996/pexels-photo-7198996.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": True,
            "position": {"x": 3, "y": 1, "z": 2},
            "expectedPosition": {"x": 3, "y": 1, "z": 2}
        },
        {
            "id": "prod-6",
            "name": "Lays Clásicas",
            "typeId": "partial",
            "imageUrl": "https://images.pexels.com/photos/4499516/pexels-photo-4499516.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 3, "y": 2, "z": 2},
            "expectedPosition": {"x": 3, "y": 3, "z": 2}
        },
        {
            "id": "prod-7",
            "name": "Takis Fuego",
            "typeId": "non-compliant",
            "imageUrl": "https://images.pexels.com/photos/8774477/pexels-photo-8774477.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 4, "y": 1, "z": 2},
            "expectedPosition": {"x": 4, "y": 2, "z": 2}
        },
        {
            "id": "prod-8",
            "name": "Agua Bioleve",
            "typeId": "compliant",
            "imageUrl": "https://images.pexels.com/photos/2983100/pexels-photo-2983100.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": True,
            "position": {"x": 5, "y": 1, "z": 3},
            "expectedPosition": {"x": 5, "y": 1, "z": 3}
        },
        {
            "id": "prod-9",
            "name": "Agua Bioleve 6 Pack",
            "typeId": "partial",
            "imageUrl": "https://images.pexels.com/photos/2983101/pexels-photo-2983101.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 5, "y": 2, "z": 3},
            "expectedPosition": {"x": 5, "y": 3, "z": 3}
        },
        {
            "id": "prod-10",
            "name": "Agua Vitawa 1L",
            "typeId": "non-compliant",
            "imageUrl": "https://images.pexels.com/photos/6103469/pexels-photo-6103469.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "isCorrectPosition": False,
            "position": {"x": 6, "y": 1, "z": 3},
            "expectedPosition": {"x": 6, "y": 2, "z": 3}
        }
    ]

    product_types = [
        {"id": "found", "name": "Productos Encontrados", "count": 45},
        {"id": "misplaced", "name": "Productos Mal Ubicados", "count": 28},
        {"id": "missing", "name": "Productos No Encontrados", "count": 32}
    ]

    positions = [
        {
            "id": "pos-1",
            "barcode": "7501045400846",
            "name": "Atun Dolores aceite 295gr lata",
            "shelf": 1,
            "position": 1,
            "facings": 1,
            "height": 5.00,
            "width": 10.00,
            "depth": 2.00,
            "currentShelf": 1,
            "currentPosition": 2,
            "currentFacings": 1,
            "currentHeight": 5.00,
            "currentWidth": 10.00,
            "currentDepth": 2.00
        }
    ]

    planogram_images = [
        "https://images.pexels.com/photos/6071198/pexels-photo-6071198.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "https://images.pexels.com/photos/3724014/pexels-photo-3724014.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "https://images.pexels.com/photos/693367/pexels-photo-693367.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    ]

    return {
        "metrics": {
            "total_products": len(products),
            "found_products": sum(1 for p in products if p["typeId"] == "found"),
            "misplaced_products": sum(1 for p in products if p["typeId"] == "misplaced"),
            "missing_products": sum(1 for p in products if p["typeId"] == "missing")
        },
        "compliance_counts": {pt["id"]: pt["count"] for pt in product_types},
        "products": products,
        "positions": positions,
        "analyzed_image_url": planogram_images[0],
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
