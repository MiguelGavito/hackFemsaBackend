from django.core.management.base import BaseCommand
import os
from django.conf import settings
import shutil

class Command(BaseCommand):
    help = 'Configura los directorios de medios y copia las imágenes de productos'

    def handle(self, *args, **options):
        # Crear directorio de medios si no existe
        media_root = settings.MEDIA_ROOT
        os.makedirs(media_root, exist_ok=True)
        
        # Crear directorios para uploads y productos
        uploads_dir = os.path.join(media_root, 'uploads')
        products_dir = os.path.join(media_root, 'products')
        
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(products_dir, exist_ok=True)
        
        self.stdout.write(self.style.SUCCESS('Directorios de medios creados correctamente'))
        
        # Aquí deberías copiar las imágenes de productos desde tu directorio de assets
        # Por ejemplo:
        # assets_dir = os.path.join(settings.BASE_DIR, 'assets', 'products')
        # if os.path.exists(assets_dir):
        #     for image in os.listdir(assets_dir):
        #         src = os.path.join(assets_dir, image)
        #         dst = os.path.join(products_dir, image)
        #         shutil.copy2(src, dst)
        #     self.stdout.write(self.style.SUCCESS('Imágenes de productos copiadas correctamente')) 