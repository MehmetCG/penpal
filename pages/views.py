from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.hashers import make_password
from django.conf.global_settings import LANGUAGES
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from django_countries import countries
from .models import Profile, User
from .serializers import ProfileReadSerializer, UserSerializer, ProfileWriteSerializer


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["languages"] = LANGUAGES
       context["countries"] = countries
       return context


class ProfileDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = "login"
    template_name = "profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(
            object=self.object, languages=LANGUAGES, countries=countries
        )
        return self.render_to_response(context)

    def has_permission(self):
        return self.request.user == self.get_object()


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        password = request.data["password"]
        request.data["password"] = make_password(password)
        return super().post(request, *args, **kwargs)


class ProfileFilter(filters.FilterSet):
    min_age = filters.NumberFilter(field_name='age', lookup_expr='gte')
    max_age = filters.NumberFilter(field_name='age', lookup_expr='lte')

    class Meta:
        model = Profile
        fields = [
            "gender", "country", "native_language", "practising_language"
        ]


class ProfileListView(ListAPIView):
    queryset = Profile.objects.filter(country__isnull=False)
    serializer_class = ProfileReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter


class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileWriteSerializer
    queryset = Profile.objects.all()
    lookup_field = "user__username"
    lookup_url_kwarg = "username"