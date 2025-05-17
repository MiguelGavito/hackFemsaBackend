from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def get_mock_products():
    ids = [
        "aceite_bebe_mennen",
        "aceite_nutrioli_400ml",
        "aceite_nutrioli_850ml",
        "aceite_posada",
        "aceite_saborsano",
        "agua_bioleve",
        "agua_bioleve_6pack",
        "agua_vitawa_1L",
        "agua_vitawa_1_5L",
        "andatti",
        "arroz_laposada",
        "atun_dolores_blanco",
        "atun_dolores_masdos",
        "atun_dolores_naranja",
        "atun_dolores_normal",
        "atun_mazatun",
        "atun_mazatun_verde",
        "azucar_laposada",
        "carnation",
        "cheetos",
        "chicharron_bitz_intenso",
        "chicharron_bitz_natural",
        "chips_sal",
        "detergente_azaela",
        "frijol_laposada",
        "frijol_lasierra",
        "lalechera",
        "leche_nutralatforte",
        "nan_nestle_1",
        "nan_nestle_2",
        "nan_nestle_3",
        "panales_tikytin_extragrande",
        "panales_tikytin_grande",
        "papel_aluminio",
        "papelhigenico_azaela_6rollos",
        "papelhigenico_azaela_amarillo",
        "papelhigenico_azaela_azul",
        "papelhigenico_kleenex_cottonelle",
        "papelhigenico_petalo",
        "papelhigenico_regio",
        "papelhigenico_suavel",
        "ruffles",
        "shampoo_bebe",
        "takis",
    ]
    return {
        "metrics": {},
        "compliance_counts": {},
        "products": [{"id": pid} for pid in ids],
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
