from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from userena import settings as userena_settings
from userena.utils import get_user_profile
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
