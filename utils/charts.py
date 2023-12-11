months = [
    "Қаңтар", "Ақпан", "Наурыз", "Сәуір",
    "Мамыр", "Маусым", "Шілде", "Тамыз",
    "Қыркүйек", "Қазан", "Қараша", "Желтоқсан"
]

weekdays = ["Дүйсенбі", "Сейсенбі", "Сәрсенбі", "Бейсенбі", "Жұма", "Сенбі", "Жексенбі"]


colorPalette = ["#55efc4", "#81ecec", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def get_day_dict():
    day_dict = dict()

    for day in weekdays:
        day_dict[day] = 0

    return day_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette