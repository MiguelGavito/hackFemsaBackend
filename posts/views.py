from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import os
from django.conf import settings
import uuid
from ultralytics import YOLO
import cv2
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

def process_image_with_yolo(image_path):
    try:
        # Cargar el modelo YOLO
        model_path = os.path.join(settings.BASE_DIR, 'posts', 'FEMSA_SEGMENTATION_DATASET_FINAL.v2i.yolov8', 'yolov8n.pt')
        model = YOLO(model_path)
        
        # Realizar la predicción
        results = model.predict(image_path, conf=0.25)
        
        # Cargar la imagen para obtener sus dimensiones
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("No se pudo cargar la imagen")
        
        height, width = img.shape[:2]
        
        # Procesar los resultados
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Obtener coordenadas del box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Calcular dimensiones relativas
                box_width = (x2 - x1) / width * 100
                box_height = (y2 - y1) / height * 100
                
                # Calcular posición relativa
                center_x = ((x1 + x2) / 2) / width * 100
                center_y = ((y1 + y2) / 2) / height * 100
                
                # Determinar el nivel del estante basado en la posición vertical
                shelf_level = int(center_y / 25) + 1  # Divide la imagen en 4 niveles
                
                # Determinar la posición horizontal
                position_x = int(center_x / 20) + 1  # Divide la imagen en 5 secciones horizontales
                
                detection = {
                    'class': int(box.cls[0].item()),
                    'confidence': float(box.conf[0].item()),
                    'box': {
                        'x1': float(x1),
                        'y1': float(y1),
                        'x2': float(x2),
                        'y2': float(y2)
                    },
                    'position': {
                        'x': position_x,
                        'y': shelf_level,
                        'z': 0
                    },
                    'dimensions': {
                        'width': box_width,
                        'height': box_height
                    }
                }
                detections.append(detection)
        
        return detections
    except Exception as e:
        print(f"Error en process_image_with_yolo: {str(e)}")
        raise

def process_detections(detections, reference_data):
    try:
        # Convertir detecciones a productos
        detected_products = []
        for det in detections:
            product = {
                'id': str(uuid.uuid4()),
                'name': f"Producto {det['class']}",
                'barcode': f"BAR-{det['class']}",
                'typeId': 'found',
                'imageUrl': f"/static/products/product_{det['class']}.jpg",
                'isCorrectPosition': True,
                'position': det['position'],
                'expectedPosition': det['position'],
                'confidence': det['confidence'],
                'dimensions': det['dimensions'],
                'box': det['box']
            }
            detected_products.append(product)
        
        # Comparar con datos de referencia
        found_products = []
        misplaced_products = []
        missing_products = []
        
        # Procesar productos encontrados y mal ubicados
        for detected in detected_products:
            found = False
            for reference in reference_data:
                if reference['name'] == detected['name']:
                    found = True
                    if (reference['position']['x'] == detected['position']['x'] and 
                        reference['position']['y'] == detected['position']['y']):
                        found_products.append(detected)
                    else:
                        detected['typeId'] = 'misplaced'
                        detected['expectedPosition'] = reference['position']
                        misplaced_products.append(detected)
                    break
            if not found:
                missing_products.append(detected)
        
        # Encontrar productos faltantes
        for reference in reference_data:
            found = False
            for detected in detected_products:
                if reference['name'] == detected['name']:
                    found = True
                    break
            if not found:
                missing_product = {
                    'id': str(uuid.uuid4()),
                    'name': reference['name'],
                    'barcode': reference['barcode'],
                    'typeId': 'missing',
                    'imageUrl': reference['imageUrl'],
                    'isCorrectPosition': False,
                    'position': {'x': 0, 'y': 0, 'z': 0},
                    'expectedPosition': reference['position'],
                    'dimensions': reference['dimensions']
                }
                missing_products.append(missing_product)
        
        return {
            'found': found_products,
            'misplaced': misplaced_products,
            'missing': missing_products
        }
    except Exception as e:
        print(f"Error en process_detections: {str(e)}")
        raise

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
        
        try:
            # Procesar la imagen con YOLO
            detections = process_image_with_yolo(image_path)
            
            # Procesar las detecciones y obtener productos
            products = process_detections(detections, get_reference_data())
            
            # Calcular métricas
            total_products = len(get_reference_data())  # Total de productos esperados
            found_products = sum(1 for p in products if p["typeId"] == "found")
            misplaced_products = sum(1 for p in products if p["typeId"] == "misplaced")
            missing_products = sum(1 for p in products if p["typeId"] == "missing")
            
            response_data = {
                "metrics": {
                    "total_products": total_products,
                    "found_products": found_products,
                    "misplaced_products": misplaced_products,
                    "missing_products": missing_products
                },
                "compliance_counts": {
                    "found": found_products,
                    "misplaced": misplaced_products,
                    "missing": missing_products
                },
                "products": products,
                "analyzed_image_url": f"/media/uploads/{image_name}",
                "detection_boxes": detections
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            logger.error(f"Error procesando imagen: {str(e)}")
            return JsonResponse({'error': 'Error procesando la imagen'}, status=500)
        
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Inicializar las imágenes de productos al cargar el módulo
setup_product_images()
