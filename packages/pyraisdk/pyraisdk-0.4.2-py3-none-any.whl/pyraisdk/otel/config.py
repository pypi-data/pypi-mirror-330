import os
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_ENDPOINT

OTEL_SCOPE						= "fa65c9d1-e75e-4ac1-b7c1-608189fd7969/.default"
OPEN_TELEMETRY_AZURE_TENANT_ID	= "33e01921-4d64-4f8c-a055-5bdaffd5e33d"
OPEN_TELEMETRY_AZURE_CLIENT_ID	= "9c7ae59d-9323-4423-a0da-38ddce774875"
OTEL_SECRET_NAME         		= "OTEL-AZURE-CLIENT-SECRET"
NON_PROD_ENDPOINT				= "https://ca-otelcol-lgvgvhiuark32.nicefield-824a522d.westus3.azurecontainerapps.io"
REGION_ENDPOINT_MAP = {
	"australiaeast":      "https://ca-otelcol-fu2wlmjxu6b6e.yellowpond-f43e443a.australiaeast.azurecontainerapps.io",
	"brazilsouth":        "https://ca-otelcol-d3f5tryi4khz4.wittydune-140850cc.eastus.azurecontainerapps.io",
	"canadacentral":      "https://ca-otelcol-d3f5tryi4khz4.wittydune-140850cc.eastus.azurecontainerapps.io",
	"canadaeast":         "https://ca-otelcol-b4mc67xirb4og.purplerock-0c0b5e25.eastus2.azurecontainerapps.io",
	"centralus":          "https://ca-otelcol-xrkbu2g2mltju.kindcoast-70aeac4c.northcentralus.azurecontainerapps.io",
	"eastus":             "https://ca-otelcol-d3f5tryi4khz4.wittydune-140850cc.eastus.azurecontainerapps.io",
	"eastus2":            "https://ca-otelcol-b4mc67xirb4og.purplerock-0c0b5e25.eastus2.azurecontainerapps.io",
	"francecentral":      "https://ca-otelcol-x4yn76z33dtmk.yellowfield-08887084.francecentral.azurecontainerapps.io",
	"germanywestcentral": "https://ca-otelcol-ob6bzjhovqcmm.gentlemushroom-5232521b.switzerlandnorth.azurecontainerapps.io",
	"italynorth":         "https://ca-otelcol-x4yn76z33dtmk.yellowfield-08887084.francecentral.azurecontainerapps.io",
	"japaneast":          "https://ca-otelcol-wnq4b4clvo5qo.livelytree-980387c1.japaneast.azurecontainerapps.io",
	"japanwest":          "https://ca-otelcol-wnq4b4clvo5qo.livelytree-980387c1.japaneast.azurecontainerapps.io",
	"koreacentral":       "https://ca-otelcol-wnq4b4clvo5qo.livelytree-980387c1.japaneast.azurecontainerapps.io",
	"northcentralus":     "https://ca-otelcol-xrkbu2g2mltju.kindcoast-70aeac4c.northcentralus.azurecontainerapps.io",
	"northeurope":        "https://ca-otelcol-zufbncfkibvcs.orangetree-1693bf70.norwayeast.azurecontainerapps.io",
	"norwayeast":         "https://ca-otelcol-zufbncfkibvcs.orangetree-1693bf70.norwayeast.azurecontainerapps.io",
	"polandcentral":      "https://ca-otelcol-ob6bzjhovqcmm.gentlemushroom-5232521b.switzerlandnorth.azurecontainerapps.io",
	"spaincentral":       "https://ca-otelcol-x4yn76z33dtmk.yellowfield-08887084.francecentral.azurecontainerapps.io",
	"southafricanorth":   "https://ca-otelcol-u7w3skx2x3plg.calmwater-14414417.uaenorth.azurecontainerapps.io",
	"southcentralus":     "https://ca-otelcol-xrkbu2g2mltju.kindcoast-70aeac4c.northcentralus.azurecontainerapps.io",
	"southeastasia":      "https://ca-otelcol-fu2wlmjxu6b6e.yellowpond-f43e443a.australiaeast.azurecontainerapps.io",
	"southindia":         "https://ca-otelcol-u7w3skx2x3plg.calmwater-14414417.uaenorth.azurecontainerapps.io",
	"swedencentral":      "https://ca-otelcol-f7rz3xrv52vku.jollyground-2660d762.swedencentral.azurecontainerapps.io",
	"switzerlandnorth":   "https://ca-otelcol-ob6bzjhovqcmm.gentlemushroom-5232521b.switzerlandnorth.azurecontainerapps.io",
	"switzerlandwest":    "https://ca-otelcol-ob6bzjhovqcmm.gentlemushroom-5232521b.switzerlandnorth.azurecontainerapps.io",
	"uaenorth":           "https://ca-otelcol-u7w3skx2x3plg.calmwater-14414417.uaenorth.azurecontainerapps.io",
	"uksouth":            "https://ca-otelcol-dc3tgx3lxrll6.blueforest-317e4693.uksouth.azurecontainerapps.io",
	"westeurope":         "https://ca-otelcol-dc3tgx3lxrll6.blueforest-317e4693.uksouth.azurecontainerapps.io",
	"westus":             "https://ca-otelcol-cfze7gvkpc75w.kindsand-35b5faaf.westus.azurecontainerapps.io",
	"westus2":            "https://ca-otelcol-3jd7tyz6qxvwa.salmonpond-3d89a275.westus2.azurecontainerapps.io",
	"westus3":            "https://ca-otelcol-lgvgvhiuark32.nicefield-824a522d.westus3.azurecontainerapps.io",
}

class OtelConfig:
	def __init__(self):
		self.environment = os.environ.get("ENVIRONMENT", "").lower()
		self.region = os.environ.get("REGION", "").lower()
		self.local_run = os.environ.get("OTEL_LOCAL", "").lower() == "true"
		self.uai_client_id = os.environ.get("UAI_CLIENT_ID", os.environ.get("AZURE_CLIENT_ID", ""))
		self.auth_scope = OTEL_SCOPE

		# The tenant id and client id are used in Test/Dev/PPE environment to fetch AAD token
		# of the OpenTelemetry collector. These two IDs will not be configurable because this is
		# the only AME client id (app id) we get whitelisted. In Prod env, we will use the RAIUAI managed
		# identity to fetch the token.
		self.azure_tenant_id = OPEN_TELEMETRY_AZURE_TENANT_ID
		self.azure_client_id = OPEN_TELEMETRY_AZURE_CLIENT_ID

		kv_suffix = self.environment if self.environment != "" else "dev"
		self.kv_url =  "https://raiglobal" + kv_suffix + "kv.vault.azure.net"
		self.kv_secret_name = OTEL_SECRET_NAME
		
		self.endpoint = os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, "")
		if self.endpoint == "":
			if self.environment == "" or self.environment == "test" or self.environment == "dev" or self.environment == "ppe":
				self.endpoint = NON_PROD_ENDPOINT
			elif self.region in REGION_ENDPOINT_MAP:
				self.endpoint = REGION_ENDPOINT_MAP[self.region]
    
	def is_active(self) -> bool:
		return self.endpoint != ""