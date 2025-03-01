from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.openapi.spec import Components, SecurityScheme

openapi_config = OpenAPIConfig(
        components=[
            Components(
                security_schemes={
                    "JWT": SecurityScheme(
                        type="http",
                        scheme="Bearer",
                        name="Authorization",
                        security_scheme_in="cookie",
                        bearer_format="JWT",
                        description="Authorization",
                    )
                }
            )
        ],
        title="Service template",
        version="1.0.0",
        path="/docs",
        root_schema_site="elements",
        render_plugins=[ScalarRenderPlugin()],
    )
