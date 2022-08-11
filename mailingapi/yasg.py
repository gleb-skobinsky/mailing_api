from django.urls import path
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class Gen(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(Gen, self).get_schema(request=request, public=public)
        if "Client" in schema.definitions.keys():
            schema.definitions["Client"]["properties"]["phone_number"][
                "example"
            ] = "79850000000"
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Django Mailing",
        default_version="v1",
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=Gen,
)

urlpatterns = [
    path(
        "swagger?format=json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
