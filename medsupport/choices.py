from model_utils import Choices

NEED_UNITS = Choices(
    ('pieces', 'шт'),
    ('packs', 'уп'),
    ('vials', 'фл'),
)

REGION = Choices(
    (0, "----"),
    (1, "Вінницька область"),
    (2, "Волинська область"),
    (3, "Дніпропетровська область"),
    (4, "Донецька область"),
    (5, "Житомирська область"),
    (6, "Закарпатська область"),
    (7, "Запорізька область"),
    (8, "Івано-Франківська область"),
    (9, "Київська область"),
    (10, "Кіровоградська область"),
    (11, "Луганська область"),
    (12, "Львівська область"),
    (13, "Миколаївська область"),
    (14, "Одеська область"),
    (15, "Полтавська область"),
    (16, "Рівненська область"),
    (17, "Сумська область"),
    (18, "Тернопільська область"),
    (19, "Харківська область"),
    (20, "Херсонська область"),
    (21, "Хмельницька область"),
    (22, "Черкаська область"),
    (23, "Чернівецька область"),
    (24, "Чернігівська область"),
    (25, "м. Київ"),
)
