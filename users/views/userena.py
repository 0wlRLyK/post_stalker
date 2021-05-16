
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from guardian.decorators import permission_required_or_403
from userena import settings as userena_settings
from userena import signals as userena_signals
from userena.decorators import secure_required
from userena.forms import (
    AuthenticationForm,
    ChangeEmailForm,
)
from userena.utils import get_user_profile, signin_redirect
from userena.views import ExtraContextTemplateView


def profile_detail(
        request,
        uid,
        template_name=userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE,
        extra_context=None,
        **kwargs
):
    """
    Detailed view of an user.

    :param uid:
        User id

    :param template_name:
        String representing the template name that should be used to display
        the profile.

    :param extra_context:
        Dictionary of variables which should be supplied to the template. The
        ``profile`` key is always the current profile.

    **Context**

    ``profile``
        Instance of the currently viewed ``Profile``.

    """
    user = get_object_or_404(get_user_model(), id=uid)
    profile = get_user_profile(user=user)
    if not profile.can_view_profile(request.user):
        raise PermissionDenied
    if not extra_context:
        extra_context = dict()
    extra_context["profile"] = profile
    extra_context["hide_email"] = userena_settings.USERENA_HIDE_EMAIL
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


def profile_detail_current_user(
        request,
        template_name=userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE,
        extra_context=None,
        **kwargs
):
    """
    Detailed view of an user.

    :param template_name:
        String representing the template name that should be used to display
        the profile.

    :param extra_context:
        Dictionary of variables which should be supplied to the template. The
        ``profile`` key is always the current profile.

    **Context**

    ``profile``
        Instance of the currently viewed ``Profile``.

    """
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), id=request.user.id)
        profile = get_user_profile(user=user)
        if not profile.can_view_profile(request.user):
            raise PermissionDenied
        if not extra_context:
            extra_context = dict()
        extra_context["profile"] = profile
        extra_context["hide_email"] = userena_settings.USERENA_HIDE_EMAIL
        return ExtraContextTemplateView.as_view(
            template_name=template_name, extra_context=extra_context
        )(request)
    return HttpResponseForbidden("Для просмотра профиля войдите либо зарегистрируйтесь!")


@secure_required
def signin(
        request,
        auth_form=AuthenticationForm,
        template_name="userena/signin_form.html",
        redirect_field_name=REDIRECT_FIELD_NAME,
        redirect_signin_function=signin_redirect,
        extra_context=None,
):
    """
    Signin using email or username with password.

    Signs a user in by combining email/username with password. If the
    combination is correct and the user :func:`is_active` the
    :func:`redirect_signin_function` is called with the arguments
    ``REDIRECT_FIELD_NAME`` and an instance of the :class:`User` who is is
    trying the login. The returned value of the function will be the URL that
    is redirected to.

    A user can also select to be remembered for ``USERENA_REMEMBER_DAYS``.

    :param auth_form:
        Form to use for signing the user in. Defaults to the
        :class:`AuthenticationForm` supplied by userena.

    :param template_name:
        String defining the name of the template to use. Defaults to
        ``userena/signin_form.html``.

    :param redirect_field_name:
        Form field name which contains the value for a redirect to the
        succeeding page. Defaults to ``next`` and is set in
        ``REDIRECT_FIELD_NAME`` setting.

    :param redirect_signin_function:
        Function which handles the redirect. This functions gets the value of
        ``REDIRECT_FIELD_NAME`` and the :class:`User` who has logged in. It
        must return a string which specifies the URI to redirect to.

    :param extra_context:
        A dictionary containing extra variables that should be passed to the
        rendered template. The ``form`` key is always the ``auth_form``.

    **Context**

    ``form``
        Form used for authentication supplied by ``auth_form``.

    """
    form = auth_form()

    if request.method == "POST":
        form = auth_form(request.POST, request.FILES)
        if form.is_valid():
            identification, password, remember_me = (
                form.cleaned_data["identification"],
                form.cleaned_data["password"],
                form.cleaned_data["remember_me"],
            )
            user = authenticate(identification=identification, password=password)
            print(request.POST)
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(
                        userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400
                    )
                else:
                    request.session.set_expiry(0)

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(
                        request, _("You have been signed in."), fail_silently=True
                    )

                # send a signal that a user has signed in
                userena_signals.account_signin.send(sender=None, user=user)
                # Whereto now?
                redirect_to = redirect_signin_function(
                    request.GET.get(
                        redirect_field_name, request.POST.get(redirect_field_name)
                    ),
                    user,
                )
                if request.is_ajax():
                    return JsonResponse({"redirect_url": redirect_to})
                return HttpResponseRedirect(redirect_to)
            else:

                # If the user is inactive, despite completing the
                # activation process, show the 'Account disabled'
                # page.  Otherwise, show the 'Activation pending'
                # page to encourage activation.
                if user.userena_signup.activation_completed:
                    return redirect(
                        reverse("userena_disabled", kwargs={"username": user.username})
                    )
                else:
                    return redirect(
                        reverse(
                            "userena_activate_pending",
                            kwargs={"username": user.username},
                        )
                    )

        else:
            if request.is_ajax():
                return JsonResponse({
                    "result": False,
                    "load_html": str(form)
                })

    if not extra_context:
        extra_context = dict()
    extra_context.update(
        {
            "form": form,
            "next": request.GET.get(
                redirect_field_name, request.POST.get(redirect_field_name)
            ),
        }
    )
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


@secure_required
@permission_required_or_403("change_user")
def email_change(
        request,
        email_form=ChangeEmailForm,
        template_name="userena/email_form.html",
        success_url=None,
        extra_context=None,
):
    """
    Change email address

    :param email_form:
        Form that will be used to change the email address. Defaults to
        :class:`ChangeEmailForm` supplied by userena.

    :param template_name:
        String containing the template to be used to display the email form.
        Defaults to ``userena/email_form.html``.

    :param success_url:
        Named URL where the user will get redirected to when successfully
        changing their email address.  When not supplied will redirect to
        ``userena_email_complete`` URL.

    :param extra_context:
        Dictionary containing extra variables that can be used to render the
        template. The ``form`` key is always the form supplied by the keyword
        argument ``form`` and the ``user`` key by the user whose email address
        is being changed.

    **Context**

    ``form``
        Form that is used to change the email address supplied by ``form``.

    ``account``
        Instance of the ``Account`` whose email address is about to be changed.

    **Todo**

    Need to have per-object permissions, which enables users with the correct
    permissions to alter the email address of others.

    """
    user = get_object_or_404(get_user_model(), id=request.user.id)
    prev_email = user.email
    form = email_form(user)

    if request.method == "POST":
        print(request.is_ajax(), form.errors)
        form = email_form(user, request.POST, request.FILES)

        if form.is_valid():

            form.save()

            if success_url:
                # Send a signal that the email has changed
                userena_signals.email_change.send(
                    sender=None, user=user, prev_email=prev_email, new_email=user.email
                )
                redirect_to = success_url
            else:
                redirect_to = reverse(
                    "userena_email_change_complete", kwargs={"username": user.username}
                )
            if request.is_ajax():
                return JsonResponse({"redirect_url": redirect_to})
            return redirect(redirect_to)
        else:
            return JsonResponse({"errors": str(form.errors.as_data()["email"])})

    if not extra_context:
        extra_context = dict()
    extra_context["form"] = form
    extra_context["profile"] = get_user_profile(user=user)
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


@secure_required
@permission_required_or_403("change_user")
def password_change(
        request,
        template_name="userena/password_form.html",
        pass_form=PasswordChangeForm,
        success_url=None,
        extra_context=None,
):
    """ Change password of user.

    This view is almost a mirror of the view supplied in
    :func:`contrib.auth.views.password_change`, with the minor change that in
    this view we also use the username to change the password. This was needed
    to keep our URLs logical (and REST) across the entire application. And
    that in a later stadium administrators can also change the users password
    through the web application itself.

    :param template_name:
        String of the name of the template that is used to display the password
        change form. Defaults to ``userena/password_form.html``.

    :param pass_form:
        Form used to change password. Default is the form supplied by Django
        itself named ``PasswordChangeForm``.

    :param success_url:
        Named URL that is passed onto a :func:`reverse` function with
        ``username`` of the active user. Defaults to the
        ``userena_password_complete`` URL.

    :param extra_context:
        Dictionary of extra variables that are passed on to the template. The
        ``form`` key is always used by the form supplied by ``pass_form``.

    **Context**

    ``form``
        Form used to change the password.

    """
    user = get_object_or_404(get_user_model(), id=request.user.id)

    form = pass_form(user=user)
    print(request.POST)

    if request.method == "POST":
        form = pass_form(user=user, data=request.POST)
        print(str(form))
        if form.is_valid():
            form.save()

            # Send a signal that the password has changed
            userena_signals.password_complete.send(sender=None, user=user)

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = reverse(
                    "userena_password_change_complete",
                    kwargs={"username": user.username},
                )
            if request.is_ajax():
                return JsonResponse({
                    "result": True,
                    "redirect_url": redirect_to
                })
            return redirect(redirect_to)
        else:
            if request.is_ajax():
                return JsonResponse({
                    "result": False,
                    "load_html": str(form)
                })

    if not extra_context:
        extra_context = dict()
    extra_context["form"] = form
    extra_context["profile"] = get_user_profile(user=user)
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)


def direct_to_user_template(request, template_name, extra_context=None):
    """
    Simple wrapper for Django's :func:`direct_to_template` view.

    This view is used when you want to show a template to a specific user. A
    wrapper for :func:`direct_to_template` where the template also has access to
    the user that is found with ``username``. For ex. used after signup,
    activation and confirmation of a new e-mail.


    :param template_name:
        String defining the name of the template to use. Defaults to
        ``userena/signup_complete.html``.

    **Keyword arguments**

    ``extra_context``
        A dictionary containing extra variables that should be passed to the
        rendered template. The ``account`` key is always the ``User``
        that completed the action.

    **Extra context**

    ``viewed_user``
        The currently :class:`User` that is viewed.

    """
    user = get_object_or_404(get_user_model(), id=request.user.id)

    if not extra_context:
        extra_context = dict()
    extra_context["viewed_user"] = user
    extra_context["profile"] = get_user_profile(user=user)
    return ExtraContextTemplateView.as_view(
        template_name=template_name, extra_context=extra_context
    )(request)
