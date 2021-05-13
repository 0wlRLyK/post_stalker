from django.http import HttpResponseNotFound, HttpResponse, JsonResponse

from users.models import User


def view_get(request, uid, permission, section_name=""):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponseNotFound("Пользователя не существует")

    if user.id == request.user.id:
        return HttpResponse(f"""
        <section id="{section_name}">
        Вы не можете перевести деньги самому себе
        </section>
        """)
    if not request.user.has_perm(permission):
        return HttpResponse(f"""
                    <section id="{section_name}">
                    У вас недостаточно прав доступа
                    </section>
                    """)
    else:
        return True


def get_user_by_id_or_response(uid):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponseNotFound("Пользователя не существует")
    else:
        return user


def get_object_or_response(item_id, item_object):
    """
    Function gets object if it exist else return Json response with error
    :param item_id: ID of passed object
    :param item_object: object
    :return: passed object if doesn't exist JSON response
    """
    try:
        obj = item_object.objects.get(id=item_id)
    except item_object.DoesNotExist:
        return JsonResponse({
            "result": False,
            "cause": "Object is doesn't exist!"
        })
    else:
        return obj, obj.cost


def get_item_cost_or_0(obj):
    if obj:
        return obj.get_sell_cost()
    return 0


def check_money(money, amount):
    if amount > money:
        return JsonResponse({
            "result": False,
            "cause": "Недостаточно денег для покупки"
        })


def sell_item(value, model, money):
    item, amount = get_object_or_response(value, model)
    check_money(money, amount)
    return item, amount
