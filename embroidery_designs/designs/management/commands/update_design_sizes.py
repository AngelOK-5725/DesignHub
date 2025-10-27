from django.core.management.base import BaseCommand
from designs.models import Design

class Command(BaseCommand):
    help = 'Update design sizes from design_size field to width/height fields'
    
    def handle(self, *args, **options):
        designs = Design.objects.all()
        for design in designs:
            if design.design_size and 'x' in design.design_size:
                try:
                    width, height = design.design_size.split('x')
                    design.design_width = int(width.strip())
                    design.design_height = int(height.strip())
                    design.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated {design.title}: {design.design_width}x{design.design_height}')
                    )
                except (ValueError, AttributeError):
                    self.stdout.write(
                        self.style.ERROR(f'Error parsing size for {design.title}: {design.design_size}')
                    )