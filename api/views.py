from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters import rest_framework as filters
from .serializers import ProfileReadSerializer, UserSerializer, ProfileWriteSerializer
from pages.models import Profile, Message


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
