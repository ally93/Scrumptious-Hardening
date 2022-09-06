from django import template

register = template.Library()


@register.filter(name="resize_to")
def resize_to(amount, serving_size):
    print("amount", amount, "serving-size", serving_size)
    if (amount and serving_size):
        new_amount = amount * float(serving_size)
        return new_amount
    else: 
        return amount
