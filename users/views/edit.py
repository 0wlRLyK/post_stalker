import sys
from io import BytesIO

from PIL import Image, ImageSequence
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.response import JsonResponse
from django.views.generic import UpdateView

from users.forms import PhotoForm
from users.models import User
from utils.views.mixins import JsonableResponseMixin


class CurrentUserMixin(object):
    model = User

    def get_object(self, *args, **kwargs):
        try:
            obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError:
            # SingleObjectMixin throws an AttributeError when no pk or slug
            # is present on the url. In those cases, we use the current user
            obj = self.request.user

        return obj


class UserEdit(CurrentUserMixin, JsonableResponseMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "birthday", "gender", "country", "state", "signature"]
    template_name = "users/edit/user_form.html"
    success_url = "/"

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.get_form()
        print(request.POST.get("signature"), request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            for key, value in form.cleaned_data.items():
                if getattr(user, key) != value:
                    print(key, value)
                    setattr(user, key, value)
                # if key == "signature":
                #
                #     signature = bleach.clean(request.POST.get("signature"))
                #     setattr(user, key, signature)
                #     print(signature)
            user.save()
            return JsonResponse({"result": True})
        return self.form_invalid(form=form, request=request)


class AvatarChanging(CurrentUserMixin, UpdateView):
    form_class = PhotoForm
    template_name = "users/edit/avatar_form.html"

    def get_context_data(self, **kwargs):
        referer = self.request.META.get('HTTP_REFERER')
        context = super().get_context_data(referer=referer, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.get_form()
        print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            name = form.cleaned_data.get('avatar').name

            image = Image.open(form.cleaned_data.get('avatar'))
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((165, 215), Image.ANTIALIAS)
            tempfile_io = BytesIO()
            if image.format in ["GIF", "WEBP"]:
                img_seq = []
                for frame in ImageSequence.Iterator(image):
                    frame.convert('RGBA')
                    frame.crop((x, y, w + x, h + y))
                    n_frame = frame.resize((165, 215), Image.ANTIALIAS)
                    img_seq.append(n_frame.copy())
                if len(img_seq) > 1:
                    resized_image = img_seq[0]
                    resized_image.save(tempfile_io, format=image.format, save_all=True, append_images=img_seq[1:],
                                       loop=0, duration=len(img_seq) / image.info['duration'] * 150, disposal=2,
                                       palette=True)
                else:
                    resized_image.save(tempfile_io, format=image.format)
            else:
                resized_image.save(tempfile_io, format=image.format)
            resized_image.save(tempfile_io, format=image.format)
            image_file = InMemoryUploadedFile(tempfile_io, None, name, image.get_format_mimetype(),
                                              sys.getsizeof(tempfile_io), None)
            user.avatar.save(name, image_file)
            user.save()
            return JsonResponse({"result": "good", "avatar": user.avatar.url})
        print(form.errors)
        return JsonResponse({"result": "bad"})
