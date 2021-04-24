from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin

from users import models as u_model
from users.forms import AddRepForm, ChoiceImageColorForm, SetStatus

U_SETTIGNS = u_model.UserSettings.load()


class ReputationDetailView(generic.DetailView, MultipleObjectMixin):
    model = u_model.User
    template_name = "users/reputation.html"
    context_object_name = "user"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = self.object.to_rep.all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ReputationCreateView(generic.CreateView):
    model = u_model.Reputation
    form_class = AddRepForm
    user_id = None
    success_url = "/"

    def get(self, request, *args, **kwargs):
        try:
            user = u_model.User.objects.get(id=int(self.kwargs["user_id"]))
        except u_model.User.DoesNotExist:
            return HttpResponseNotFound("Пользователя не существует")
        if user.id == request.user.id:
            return HttpResponse("""
            <section id="respect_changing">
            Вы не можете изменить репутацию самому себе
            </section>
            """)

    def post(self, request, *args, **kwargs):
        author = request.user
        subj = request.POST.get('subject')
        operation_type = request.POST.get('type')
        try:
            user = u_model.User.objects.get(id=int(self.kwargs["user_id"]))
        except u_model.User.DoesNotExist:
            return JsonResponse({"result": False,
                                 "cause": "Пользователя не существует"})
        if user.id == request.user.id:
            return JsonResponse({"result": False,
                                 "cause": "Вы не можете изменить репутацию самому себе"})
        value = 0
        if operation_type == "minus":
            value = -1
        elif operation_type == "plus":
            value = +1
        user.respect += value
        print(operation_type, value, subj)
        data = {
            "id": u_model.Reputation.objects.last().id + 1,
            "from_user": author,
            "to_user": user,
            "value": value,
        }
        respect = u_model.Reputation(id=data["id"], from_user=data["from_user"], to_user=data["to_user"], subject=subj,
                                     value=value)
        respect.save()
        user.save()
        print(respect, user.respect)
        return JsonResponse({"result": bool(respect),
                             "current_respect": user.respect})


class TransactionDetailView(generic.DetailView, MultipleObjectMixin):
    model = u_model.User
    template_name = "users/money_balance.html"
    context_object_name = "user"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = self.object.to_transaction.all()
        user_money = self.request.user.money
        context = super().get_context_data(object_list=object_list, user_money=user_money, **kwargs)
        return context


class TransactionCreateView(generic.CreateView):
    model = u_model.MoneyTransaction
    user_id = None
    success_url = "/"
    fields = ["value", "message"]

    def get(self, request, *args, **kwargs):
        try:
            user = u_model.User.objects.get(id=int(self.kwargs["user_id"]))
        except u_model.User.DoesNotExist:
            return HttpResponseNotFound("Пользователя не существует")
        if user.id == request.user.id:
            return HttpResponse("""
            <section id="money_transfer">
            Вы не можете перевести деньги самому себе
            </section>
            """)

    def post(self, request, *args, **kwargs):
        author = request.user
        msg = request.POST.get('message')
        value = int(request.POST.get('value'))
        if value < 0:
            return JsonResponse({"result": False,
                                 "cause": "Значение должно быть больше ноля"})
        try:
            user = u_model.User.objects.get(id=int(self.kwargs["user_id"]))
        except u_model.User.DoesNotExist:
            return JsonResponse({"result": False,
                                 "cause": "Пользователя не существует"})
        if user.id == request.user.id:
            return JsonResponse({"result": False,
                                 "cause": "Вы не можете перевести деньги самому себе"})

        if author.money < value:
            return JsonResponse({"result": False,
                                 "cause": "На вашем счету недостаточно средств для перевода"})
        author.money -= value
        user.money += value
        data = {
            "from_user": author,
            "to_user": user,
        }
        transaction = u_model.MoneyTransaction(from_user=data["from_user"], to_user=data["to_user"],
                                               message=msg,
                                               value=value)
        transaction.save()
        author.save()
        user.save()
        return JsonResponse({"result": bool(transaction),
                             "user_currency": user.money,
                             "my_currency": author.money,
                             })

    def get_context_data(self, **kwargs):
        user_money = self.request.user.money
        context = super().get_context_data(user_money=user_money, **kwargs)
        return context


class SelectChatImageView(generic.FormView):
    template_name = "users/img_select.html"
    form_class = ChoiceImageColorForm

    def get_context_data(self, **kwargs):
        settings = {"ico_price": U_SETTIGNS.chat_ico_price,
                    "color_price": U_SETTIGNS.chat_color_price}
        context = super().get_context_data(settings=settings, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        amount, icon = 0, None
        if request.POST.get('icon'):
            icon = int(request.POST.get('icon'))
        color = request.POST.get('color')
        print(bool(icon), bool(color))
        if not icon and not color:
            return JsonResponse({
                "result": False,
                "cause": "Нет данных для измения"
            })
        if icon and user.money < U_SETTIGNS.chat_ico_price:
            return JsonResponse({
                "result": False,
                "cause": f"Недостаточно {U_SETTIGNS.chat_ico_price - user.money} ДФ для изменения иконки"
            })
        elif not icon or user.ico_num == icon:
            pass
        else:
            user.ico_num = icon
            user.money -= U_SETTIGNS.chat_ico_price
            amount -= U_SETTIGNS.chat_ico_price
        if color and user.money < U_SETTIGNS.chat_color_price:
            print(U_SETTIGNS.chat_color_price, user.money)
            return JsonResponse({
                "result": False,
                "cause": f"Недостаточно {U_SETTIGNS.chat_color_price - user.money} ДФ для изменения цвета"
            })
        elif not color or user.chat_color == color:
            pass
        else:
            user.chat_color = color
            user.money -= U_SETTIGNS.chat_color_price
            amount -= U_SETTIGNS.chat_color_price
        user.save()
        transaction = u_model.MoneyTransaction(
            from_user_id=None,
            to_user_id=user.id,
            message="Измение иконки/цвета никнейма в чате",
            value=amount
        )
        transaction.save()
        icon = user.ico_num if not icon else icon
        return JsonResponse({
            "result": True,
            "cause": "Данные успешно изменены",
            "src": f"/static/post_stalker/ico/Chat/{icon}.png",
        })


class ChangeStatusView(generic.FormView):
    form_class = SetStatus
    template_name = "users/change_status.html"

    def post(self, request, *args, **kwargs):
        status = request.POST.get("status")
        request.user.status = status
        request.user.save()
        return JsonResponse({
            "result": True,
            "status": status,
        })
