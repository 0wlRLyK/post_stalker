import bleach
from django.contrib.auth.models import Group
from django.http import response
from django.shortcuts import get_object_or_404
from django.views import generic

from users.models import User
from users.models_dir.group import Fraction, ApplicationForMembership


class FactionUsersView(generic.ListView):
    template_name = "users/faction/faction_users.html"
    context_object_name = "user_list"
    paginate_by = 30

    def get_queryset(self):
        self.group = get_object_or_404(Group, id=self.kwargs["group_id"])
        return User.objects.filter(groups__id=self.kwargs["group_id"])

    def get_context_data(self, *, object_list=None, **kwargs):
        fraction = Fraction.objects.get(group=self.group)
        context = super(FactionUsersView, self).get_context_data(fraction=fraction)
        return context


class JoinTheFraction(generic.CreateView):
    model = ApplicationForMembership
    fields = ["group", "user_message"]
    template_name = "users/faction/join_the_fraction.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            fraction = Fraction.objects.get(id=int(request.POST.get("fraction_id")), can_entry=True)
        except Fraction.DoesNotExist:
            return response.JsonResponse({
                "result": False,
                "cause": "Указанная группировка не существует, или вступление в нее запрещено!"
            })
        except ValueError:
            return response.JsonResponse({
                "result": False,
                "cause": "Неправильный тип переданного значения"
            })
        comment = bleach.clean(request.POST.get("comment"))
        app = ApplicationForMembership.objects.create(user_id=user.id, group_id=fraction.id,
                                                      user_message=comment)
        return response.JsonResponse({
            "result": True,
        })

    def get_context_data(self, **kwargs):
        user = self.request.user
        fractions = Fraction.objects.filter(can_entry=True)
        context = super().get_context_data(fractions=fractions)
        return context


class UserApplicationsForJoin(generic.ListView):
    template_name = "users/faction/user_apps.html"
    context_object_name = "apps_list"
    paginate_by = 30

    def get_queryset(self):
        get_object_or_404(User, id=self.kwargs["user_id"])
        return ApplicationForMembership.objects.filter(user_id=self.kwargs["user_id"])


class GroupApplicationsForJoin(generic.ListView):
    template_name = "users/faction/group_apps.html"
    context_object_name = "apps_list"
    paginate_by = 30

    def get_queryset(self):
        self.fraction = get_object_or_404(Fraction, id=self.kwargs["group_id"])
        return ApplicationForMembership.objects.filter(group_id=self.kwargs["group_id"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GroupApplicationsForJoin, self).get_context_data(fraction=self.fraction)
        return context


class MakeDecision(generic.View):
    decision_type = None

    def post(self, request):
        try:
            app_form = ApplicationForMembership.objects.get(id=int(request.POST.get("app_id")), archived=False)
        except ApplicationForMembership.DoesNotExist:
            return response.JsonResponse({
                "result": False,
                "cause": "Заявки не существует, либо она уже неактивна."
            })
        fraction, user = app_form.group, app_form.user
        if request.user.id not in [fraction.leader_id, fraction.deputy_leader_id]:
            return response.JsonResponse({
                "result": False,
                "cause": "Рассматривать решение о принятии в группировку может только лидер и его заместитель"
            })
        app_form.leader_message = bleach.clean(request.POST.get("message"))
        app_form.leader_id = request.user.id
        if self.decision_type == "accept":
            user.group_id = fraction.group_id
            user.groups.clear()
            user.groups.add(fraction.group)
            user.save()
            app_form.decision = True
        elif self.decision_type == "refuse":
            app_form.decision = True
        else:
            return response.JsonResponse({
                "result": False,
                "cause": "Неподдерживаемый тип решения"
            })
        app_form.archived = True
        app_form.save()
        return response.JsonResponse({
            "result": True,
        })


class ExpelUser(generic.View):
    def post(self, request):
        try:
            user = User.objects.get(id=int(request.POST.get("uid")))
        except User.DoesNotExist:
            return response.JsonResponse({
                "result": False,
                "cause": "Указанный пользователь не существует, или вступление в нее запрещено!"
            })
        except ValueError:
            return response.JsonResponse({
                "result": False,
                "cause": "Неправильный тип переданного значения"
            })
        fraction = user.get_fraction()
        if not fraction:
            return response.JsonResponse({
                "result": False,
                "cause": "Пользователь не состоит не в одной из групп"
            })
        if request.user.id not in (fraction.leader_id, fraction.deputy_leader_id):
            return response.JsonResponse({
                "result": False,
                "cause": "Изганять пользователя из группы может только лидер и его заместитель"
            })
        user.group_id = 1
        ApplicationForMembership.objects.create(user_id=user.id, group_id=fraction.id, leader_id=request.user.id,
                                                leader_message=bleach.clean(request.POST.get("message")),
                                                archived=True, banished=True)
        user.groups.clear()
        user.groups.add(Group.objects.get(id=1))
        user.save()
        return response.JsonResponse({
            "result": True
        })
