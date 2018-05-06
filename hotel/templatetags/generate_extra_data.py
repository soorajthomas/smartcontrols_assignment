from django import template

register = template.Library()


@register.filter(name='get_value')
def get_value(dict, key):
    return dict[key]


@register.filter(name='get_image_url')
def get_image_url(hotel_name):
    import random
    images = [
        'https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg',
        'https://a0.muscache.com/im/pictures/21611933/43f6de69_original.jpg',
        'https://a0.muscache.com/im/pictures/65441227/bb1eb2dd_original.jpg',
        'https://a0.muscache.com/im/pictures/52149945/33130c63_original.jpg',
        'https://a0.muscache.com/im/pictures/6722906/b4bc6418_original.jpg',
        'https://a0.muscache.com/im/pictures/812e040f-6f6f-4cae-ad67-66c050b57c1f.jpg'
    ]
    return random.choice(images)