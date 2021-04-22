from django.http import JsonResponse
from django.views import generic
from django.views.generic.list import MultipleObjectMixin

from users import models as u_model
from users.forms import AddRepForm


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

    def post(self, request, *args, **kwargs):
        author = request.user
        subj = request.POST.get('subject')
        operation_type = request.POST.get('type')

        user = u_model.User.objects.get(id=int(self.kwargs["user_id"]))

        value = 0
        if operation_type == "minus":
            value = -1
        elif operation_type == "plus":
            value = +1
        user.respect += value
        print(operation_type, value)
        data = {
            "id": u_model.Reputation.objects.last().id + 1,
            "from_user": author,
            "to_user": user,
            "value": value,
        }
        respect = u_model.Reputation(id=data["id"], from_user=data["from_user"], to_user=data["to_user"], subject=subj,
                                     value=value)
        result = respect.save()
        user.save()
        return JsonResponse({"result": bool(result),
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

    def post(self, request, *args, **kwargs):
        author = request.user
        msg = request.POST.get('message')
        print(request.POST.get('value'))
        value = int(request.POST.get('value'))

        user = u_model.User.objects.get(id=int(self.kwargs["user_id"]))

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
