# designs/management/commands/load_hoops.py

from django.core.management.base import BaseCommand
from designs.models import HoopSize

class Command(BaseCommand):
    help = 'Load default hoop sizes for Janome machines'
    
    def handle(self, *args, **options):
        hoops_data = [
            {
                'code': 'RE36b',
                'name': 'RE36b (200×360 мм)',
                'width': 200,
                'height': 360,
                'compatible_machines': 'Memory Craft 550E / 550E Limited Edition'
            },
            {
                'code': 'RE28b',
                'name': 'RE28b (200×280 мм)',
                'width': 200,
                'height': 280,
                'compatible_machines': 'Memory Craft 500E / 550E'
            },
            {
                'code': 'SQ20b',
                'name': 'SQ20b (200×200 мм)',
                'width': 200,
                'height': 200,
                'compatible_machines': 'Memory Craft 500E / 550E'
            },
            {
                'code': 'RE20b',
                'name': 'RE20b (140×200 мм)',
                'width': 140,
                'height': 200,
                'compatible_machines': 'Memory Craft 500E / 550E'
            },
            {
                'code': 'SQ14b',
                'name': 'SQ14b (140×140 мм)',
                'width': 140,
                'height': 140,
                'compatible_machines': 'Memory Craft 500E / 550E'
            },
            {
                'code': 'RE10b',
                'name': 'RE10b (100×40 мм)',
                'width': 100,
                'height': 40,
                'compatible_machines': 'Memory Craft 500E / 550E'
            },
            {
                'code': 'ASQ18b',
                'name': 'ASQ18b (184×184 мм)',
                'width': 184,
                'height': 184,
                'compatible_machines': 'MC400E/500E/550E (AcuFil)'
            },
            {
                'code': 'SQ10e',
                'name': 'SQ10e (100×100 мм)',
                'width': 100,
                'height': 100,
                'compatible_machines': 'Memory Craft 1000 / 100E'
            },
        ]
        
        for hoop_data in hoops_data:
            hoop, created = HoopSize.objects.get_or_create(
                code=hoop_data['code'],
                defaults=hoop_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created hoop: {hoop.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Hoop already exists: {hoop.name}')
                )