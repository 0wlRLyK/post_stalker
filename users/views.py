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
        context = super(ReputationDetailView, self).get_context_data(object_list=object_list, **kwargs)
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
