from django.http import HttpResponseNotFound, HttpResponse

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
