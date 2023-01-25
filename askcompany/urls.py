from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django_pydenticon.views import image as pydenticon_image

# 이게 공식 문서에 있는 import인데 이건 지원하지 않는다.
# import django_pydenticon.urls



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(TemplateView.as_view(template_name = 'root.html')), name = 'root'),
    path('accounts/', include('accounts.urls')),
    path('identicon/image/<path:data>/', pydenticon_image, name = 'pydenticon_image'),
    path('', include('instagram.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
