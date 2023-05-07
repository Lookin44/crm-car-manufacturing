from django.core.management.base import BaseCommand
from api.models import *


class Command(BaseCommand):

    help = 'Заполнение базы данных системными данными'

    def handle(self, *args, **options):

        # Создание цехов
        plastic_shop = Shop(name='PLASTIC SHOP')
        press_shop = Shop(name='PRESS SHOP')
        body_shop = Shop(name='BODY SHOP')
        paint_shop = Shop(name='PAINT SHOP')
        trim_chassis = Shop(name='TRIM & CHASSIS')
        shop_names = [
            plastic_shop,
            press_shop,
            body_shop,
            paint_shop,
            trim_chassis,
        ]
        Shop.objects.bulk_create(shop_names)

        # Создание смен
        a_shift = Shift(letter_designation='A')
        b_shift = Shift(letter_designation='B')
        c_shift = Shift(letter_designation='C')
        shift_names = [
            a_shift,
            b_shift,
            c_shift,
        ]
        Shift.objects.bulk_create(shift_names)

        # Создание участков
        tpqc = Zone(
            name='TPQC',
            description='Участок обслуживания цеха',
            shop=paint_shop,
        )
        sealing = Zone(
            name='SEALING',
            description='Участок нанесения герметика и мастики',
            shop=paint_shop,
        )
        sanding = Zone(
            name='SANDING',
            description='Участок подготовки '
                        'поверхности кузова к финальной окраске',
            shop=paint_shop,
        )
        top_coat = Zone(
            name='TOP COAT',
            description='Участок окраски кузовов',
            shop=paint_shop,
        )
        check_repair = Zone(
            name='CHECK & REPAIR',
            description='Участок полировки и ремонта кузова',
            shop=paint_shop,
        )
        bumper = Zone(
            name='BUMPER LINE',
            description='Участок окраски и полировки бамперов',
            shop=paint_shop,
        )
        zone_names = [
            tpqc,
            sealing,
            sanding,
            top_coat,
            check_repair,
            bumper
        ]
        Zone.objects.bulk_create(zone_names)

        # Создание должностей
        paint_line_operator = Position(
            name='Оператор окрасочной линии',
            grade='EVP-8',
        )
        painter = Position(
            name='Маляр',
            grade='EVP-8',
        )
        body_straightener = Position(
            name='Рихтовщик кузовов',
            grade='EVP-7',
        )
        technician_technologist = Position(
            name='Техник-технолог',
            grade='EVP-7',
        )
        team_leader = Position(
            name='Мастер',
            grade='EVP-7',
        )
        supervisor = Position(
            name='Начальник участка',
            grade='EVP-6',
        )
        engineer = Position(
            name='Инженер',
            grade='EVP-6',
        )
        senior_supervisor = Position(
            name='Начальник смены',
            grade='EVP-5',
        )
        manager = Position(
            name='Менеджер цеха',
            grade='EVP-4',
        )
        positions_names = [
            paint_line_operator,
            painter,
            body_straightener,
            technician_technologist,
            team_leader,
            supervisor,
            engineer,
            senior_supervisor,
            manager,
        ]
        Position.objects.bulk_create(positions_names)
