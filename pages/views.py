from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.hashers import make_password
from django.conf.global_settings import LANGUAGES
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
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
    slug_field = "user__username"
    slug_url_kwarg = "username"
    model = Profile

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(
            object=self.object, languages=LANGUAGES, countries=countries
        )
        return self.render_to_response(context)

    def has_permission(self):
        return self.request.user == self.get_object().user


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
    queryset = Profile.objects.all()
    serializer_class = ProfileReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(country__isnull=False) \
                                .exclude(user=self.request.user) \
                                .order_by("user__last_login")
        return queryset


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.user


class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileWriteSerializer
    queryset = Profile.objects.all()
    lookup_field = "user__username"
    lookup_url_kwarg = "username"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]