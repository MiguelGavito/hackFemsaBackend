from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import os
from django.conf import settings
import uuid
import json
import shutil

logger = logging.getLogger(__name__)

def get_reference_data():
    # Datos de referencia para cada producto
    reference_products = {
        "aceite_saborsano": {
            "id": 4,
            "name": "Sabrosano Mantequila 850 ml",
            "barcode": "7501039122099",
            "shelf": 3,
            "position": 6,
            "facings": 1,
            "dimensions": {
                "height": 25.80,
                "width": 7.20,
                "depth": 2.00
            }
        },
        "atun_mazatun": {
            "id": 15,
            "name": "Atun Mazatun Agua Sin Soya 130grs",
            "barcode": "7501045404271",
            "shelf": 1,
            "position": 3,
            "facings": 1,
            "dimensions": {
                "height": 3.39,
                "width": 8.57,
                "depth": 2.00
            }
        },
        "papel_aluminio": {
            "id": 33,
            "name": "Papel aluminio festivo rollo 76 m X 30 cm pz",
            "barcode": "7501954903421",
            "shelf": 1,
            "position": 7,
            "facings": 1,
            "dimensions": {
                "height": 31.50,
                "width": 5.00,
                "depth": 5.00
            }
        },
        "lalechera": {
            "id": 26,
            "name": "La Lechera Sirve Facil 335gr Bote",
            "barcode": "7501059278868",
            "shelf": 2,
            "position": 3,
            "facings": 1,
            "dimensions": {
                "height": 14.50,
                "width": 7.50,
                "depth": 2.00
            }
        },
        "andatti": {
            "id": 9,
            "name": "Cafe Soluble Andatti 275g",
            "barcode": "7502271155920",
            "shelf": 3,
            "position": 2,
            "facings": 1,
            "dimensions": {
                "height": 21.00,
                "width": 9.80,
                "depth": 2.00
            }
        },
        "azucar_laposada": {
            "id": 17,
            "name": "Azucar Estandar La Posada 1 kg",
            "barcode": "7502271156736",
            "shelf": 2,
            "position": 5,
            "facings": 1,
            "dimensions": {
                "height": 13.50,
                "width": 22.50,
                "depth": 3.50
            }
        },
        "atun_dolores_blanco": {
            "id": 11,
            "name": "Atun Dolores aceite 295gr lata",
            "barcode": "7501045400846",
            "shelf": 1,
            "position": 1,
            "facings": 1,
            "dimensions": {
                "height": 5.00,
                "width": 10.00,
                "depth": 2.00
            }
        },
        "atun_dolores_masdos": {
            "id": 12,
            "name": "ATUN DOLORES EN ACEITE 130GRS",
            "barcode": "7501045403014",
            "shelf": 1,
            "position": 2,
            "facings": 1,
            "dimensions": {
                "height": 3.30,
                "width": 8.50,
                "depth": 8.50
            }
        },
        "atun_dolores_normal": {
            "id": 14,
            "name": "Atun Dorado Aceite 285grs",
            "barcode": "7501045403823",
            "shelf": 1,
            "position": 20,
            "facings": 1,
            "dimensions": {
                "height": 4.75,
                "width": 10.15,
                "depth": 2.00
            }
        },
        "atun_dolores_naranja": {
            "id": 13,
            "name": "Ensalada Atun Mazatun CupCan",
            "barcode": "7501045402833",
            "shelf": 1,
            "position": 6,
            "facings": 1,
            "dimensions": {
                "height": 4.70,
                "width": 8.90,
                "depth": 2.00
            }
        },
        "shampoo_bebe": {
            "id": 42,
            "name": "Shampoo KleenBebe Manzanilla 250ml",
            "barcode": "7506425651061",
            "shelf": 7,
            "position": 2,
            "facings": 1,
            "dimensions": {
                "height": 18.20,
                "width": 7.40,
                "depth": 4.50
            }
        },
        "aceite_nutrioli_400ml": {
            "id": 1,
            "name": "ACEITE NUTRIOLI 400 ML",
            "barcode": "7501039121993",
            "shelf": 3,
            "position": 5,
            "facings": 1,
            "dimensions": {
                "height": 21.30,
                "width": 6.80,
                "depth": 2.00
            }
        },
        "aceite_nutrioli_850ml": {
            "id": 2,
            "name": "Aceite Comestible Nutrioli 850ml",
            "barcode": "7501039121610",
            "shelf": 3,
            "position": 4,
            "facings": 1,
            "dimensions": {
                "height": 26.00,
                "width": 8.00,
                "depth": 2.00
            }
        },
        "aceite_bebe_mennen": {
            "id": 0,
            "name": "Aceite para bebe Baby Magic Mennen 100 ml bote",
            "barcode": "7501035908246",
            "shelf": 7,
            "position": 1,
            "facings": 1,
            "dimensions": {
                "height": 12.50,
                "width": 5.20,
                "depth": 3.30
            }
        },
        "chips_sal": {
            "id": 22,
            "name": "Papas Chips Barcel 170 gr bolsa con sal",
            "barcode": "7501000266203",
            "shelf": 4,
            "position": 5,
            "facings": 1,
            "dimensions": {
                "height": 31.00,
                "width": 19.00,
                "depth": 5.00
            }
        },
        "frijol_lasierra": {
            "id": 25,
            "name": "Frijol La Sierra Chorizo 430 bolsa",
            "barcode": "7501052421391",
            "shelf": 3,
            "position": 7,
            "facings": 1,
            "dimensions": {
                "height": 18.90,
                "width": 13.60,
                "depth": 2.00
            }
        },
        "nan_nestle_1": {
            "id": 28,
            "name": "NAN 1 OPTIPRO Formula Infantil 12x400gMX",
            "barcode": "7501058623188",
            "shelf": 7,
            "position": 6,
            "facings": 1,
            "dimensions": {
                "height": 14.30,
                "width": 10.00,
                "depth": 10.00
            }
        },
        "nan_nestle_2": {
            "id": 29,
            "name": "NAN 2 OPTIPRO Formula Infantil 12x400gMX",
            "barcode": "7501058623195",
            "shelf": 7,
            "position": 7,
            "facings": 1,
            "dimensions": {
                "height": 14.30,
                "width": 10.00,
                "depth": 10.00
            }
        }
    }
    return reference_products

def get_mock_detections():
    # Datos de ejemplo basados en el formato del algoritmo
    detections = [
        {
            "class_id": 4,
            "class_name": "aceite_saborsano",
            "confidence": 0.7944524884223938,
            "box": {
                "x1": 588.0408935546875,
                "y1": 586.5037231445312,
                "x2": 663.5117797851562,
                "y2": 830.723876953125
            }
        },
        {
            "class_id": 15,
            "class_name": "atun_mazatun",
            "confidence": 0.771377444267273,
            "box": {
                "x1": 448.7502136230469,
                "y1": 1246.7755126953125,
                "x2": 532.0804443359375,
                "y2": 1329.2236328125
            }
        }
    ]
    return detections

def get_product_image_path(product_name):
    # Mapeo de nombres de productos a nombres de archivo de imagen
    image_mapping = {
        "aceite_saborsano": "aceite_saborsano.jpg",
        "atun_mazatun": "atun_mazatun.jpg",
        "papel_aluminio": "papel_aluminio.jpg",
        "lalechera": "lalechera.jpg",
        "andatti": "andatti.jpg",
        "azucar_laposada": "azucar_laposada.jpg",
        "atun_dolores_blanco": "atun_dolores_blanco.jpg",
        "atun_dolores_masdos": "atun_dolores_masdos.jpg",
        "atun_dolores_normal": "atun_dolores_normal.jpg",
        "atun_dolores_naranja": "atun_dolores_naranja.jpg",
        "shampoo_bebe": "shampoo_bebe.jpg",
        "aceite_nutrioli_400ml": "aceite_nutrioli_400ml.jpg",
        "aceite_nutrioli_850ml": "aceite_nutrioli_850ml.jpg",
        "aceite_bebe_mennen": "aceite_bebe_mennen.jpg",
        "chips_sal": "chips_sal.jpg",
        "frijol_lasierra": "frijol_lasierra.jpg",
        "nan_nestle_1": "nan_nestle_1.jpg",
        "nan_nestle_2": "nan_nestle_2.jpg"
    }
    
    # Obtener el nombre del archivo de imagen o usar una imagen por defecto
    image_filename = image_mapping.get(product_name, "default_product.jpg")
    return f"/media/products/{image_filename}"

def setup_product_images():
    # Crear directorio para imágenes de productos si no existe
    products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    os.makedirs(products_dir, exist_ok=True)
    
    # Crear una imagen por defecto si no existe
    default_image_path = os.path.join(products_dir, 'default_product.jpg')
    if not os.path.exists(default_image_path):
        # Aquí podrías copiar una imagen por defecto desde un directorio de assets
        pass

def process_detections(detections):
    reference_data = get_reference_data()
    products = []
    found_classes = set()
    
    for detection in detections:
        class_name = detection['class_name']
        if class_name not in reference_data:
            continue
            
        ref = reference_data[class_name]
        
        # Convertir las coordenadas de la caja a posición relativa
        x_center = (detection['box']['x1'] + detection['box']['x2']) / 2
        y_center = (detection['box']['y1'] + detection['box']['y2']) / 2
        
        # Determinar el nivel (shelf) basado en la coordenada y
        if y_center < 500:
            detected_shelf = 4  # Nivel superior
        elif y_center < 800:
            detected_shelf = 3
        elif y_center < 1100:
            detected_shelf = 2
        else:
            detected_shelf = 1  # Nivel inferior
            
        # Determinar la posición horizontal
        detected_position = int(x_center / 200) + 1  # Dividir la imagen en secciones de 200px
        
        # Verificar si está en la posición correcta
        is_correct_position = (detected_shelf == ref['shelf'] and 
                             detected_position == ref['position'])
        
        product = {
            "id": f"prod-{detection['class_id']}",
            "name": ref['name'],
            "barcode": ref['barcode'],
            "typeId": "found" if is_correct_position else "misplaced",
            "imageUrl": get_product_image_path(class_name),
            "isCorrectPosition": is_correct_position,
            "position": {
                "x": detected_position,
                "y": detected_shelf,
                "z": 1
            },
            "expectedPosition": {
                "x": ref['position'],
                "y": ref['shelf'],
                "z": 1
            },
            "confidence": detection['confidence'],
            "dimensions": ref['dimensions']
        }
        products.append(product)
        found_classes.add(detection['class_id'])
    
    # Generar productos faltantes (missing)
    for class_name, ref in reference_data.items():
        if ref['id'] not in found_classes:
            product = {
                "id": f"prod-{ref['id']}",
                "name": ref['name'],
                "barcode": ref['barcode'],
                "typeId": "missing",
                "imageUrl": get_product_image_path(class_name),
                "isCorrectPosition": False,
                "position": {"x": 0, "y": 0, "z": 0},
                "expectedPosition": {
                    "x": ref['position'],
                    "y": ref['shelf'],
                    "z": 1
                },
                "dimensions": ref['dimensions']
            }
            products.append(product)
    
    return products

def get_mock_products():
    # Estado inicial sin imagen subida
    return {
        "metrics": {
            "total_products": 0,
            "found_products": 0,
            "misplaced_products": 0,
            "missing_products": 0
        },
        "compliance_counts": {
            "found": 0,
            "misplaced": 0,
            "missing": 0
        },
        "products": [],
        "analyzed_image_url": "",
        "detection_boxes": [],
        "classes": [{"id": f"class_{i}", "name": f"Clase {i}", "detected": False, "position": {"x": 0, "y": 0, "z": 0}, "confidence": 0.0} for i in range(1, 45)]
    }

def planograma_analisis(request):
    logger.info('GET /api/planograma/analisis/ called')
    return JsonResponse(get_mock_products())

@csrf_exempt
def planograma_analizar_imagen(request):
    if request.method == 'POST':
        logger.info('POST /api/planograma/analizar-imagen/ called')
        
        # Verificar si hay una imagen en la petición
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No se proporcionó ninguna imagen'}, status=400)
        
        image = request.FILES['image']
        
        # Generar un nombre único para la imagen
        image_name = f"{uuid.uuid4()}_{image.name}"
        
        # Crear el directorio de uploads si no existe
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Guardar la imagen
        image_path = os.path.join(upload_dir, image_name)
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        logger.info(f'Imagen guardada en: {image_path}')
        
        # Obtener detecciones y procesar datos
        detections = get_mock_detections()
        products = process_detections(detections)
        
        product_types = [
            {"id": "found", "name": "Productos Encontrados", "count": len([p for p in products if p["typeId"] == "found"])},
            {"id": "misplaced", "name": "Productos Mal Ubicados", "count": len([p for p in products if p["typeId"] == "misplaced"])},
            {"id": "missing", "name": "Productos No Encontrados", "count": len([p for p in products if p["typeId"] == "missing"])}
        ]
        
        response_data = {
            "metrics": {
                "total_products": len(products),
                "found_products": len([p for p in products if p["typeId"] == "found"]),
                "misplaced_products": len([p for p in products if p["typeId"] == "misplaced"]),
                "missing_products": len([p for p in products if p["typeId"] == "missing"])
            },
            "compliance_counts": {pt["id"]: pt["count"] for pt in product_types},
            "products": products,
            "analyzed_image_url": f'/media/uploads/{image_name}',
            "detection_boxes": detections,
            "classes": [{"id": f"class_{i}", "name": f"Clase {i}", "detected": False, "position": {"x": 0, "y": 0, "z": 0}, "confidence": 0.0} for i in range(1, 45)]
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Inicializar las imágenes de productos al cargar el módulo
setup_product_images()
