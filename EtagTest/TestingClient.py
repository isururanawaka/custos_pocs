import logging
import os
from clients.user_management_client import UserManagementClient
from clients.identity_management_client import IdentityManagementClient
from clients.tenant_management_client import TenantManagementClient
from clients.resource_secret_management_client import ResourceSecretManagementClient

from transport.settings import CustosServerClientSettings
import clients.utils.utilities as utl

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# load APIServerClient with default configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings_path = os.path.join(BASE_DIR, "transport", "settings.ini")

user_client = UserManagementClient(configuration_file_location=settings_path)
id_client = IdentityManagementClient(configuration_file_location=settings_path)
secret_client = ResourceSecretManagementClient(configuration_file_location=settings_path)
tenant_client = TenantManagementClient()

custos_settings = CustosServerClientSettings(configFileLocation=settings_path)

token = utl.get_token(custos_settings=custos_settings)


def register_etag_gateway():
    contacts = ["+8123946793"]
    redirect_uris = ["http://localhost:8080/callback,http://localhost/callback"]
    response = tenant_client.create_admin_tenant(client_name="Etag gateway",
                                                 requester_email="isjarana@iu.edu",
                                                 admin_frist_name="Jhon",
                                                 admin_last_name="Smith",
                                                 admin_email="isjarana@iu.edu",
                                                 admin_username="admin",
                                                 admin_password="1234",
                                                 contacts=contacts,
                                                 redirect_uris=redirect_uris,
                                                 client_uri="https://etag.scigap.org/",
                                                 scope="openid profile email org.cilogon.userinfo",
                                                 domain="etag.scigap.org",
                                                 logo_uri="https://etag.org/static/favicon.png",
                                                 comment="Etag Portal")

    # respose = {
    #     "client_id": "custos-xlbkovs0nuvhfdbw7bzh-10000402",
    #     "client_secret": "3uX6fnvMtR2xr0BpYsetTbqWBZVC8B1whsBRUCMA",
    #     "client_id_issued_at": 1.588339802e+12,
    #     "registration_client_uri": "https://custos.scigap.org:32036/tenant-management/v1.0.0/oauth2/tenant?client_id=custos-xlbkovs0nuvhfdbw7bzh-10000402",
    #     "msg": "Use Base64 encoded clientId:clientSecret as auth token for authorization, Credentials are activated after admin approval",
    #     "token_endpoint_auth_method": "client_secret_basic"
    # }


# Register user , but is not activated. After registration client should send an email to
# user for validation, once validated, user should be enabled to activate
def register_user():
    response = user_client.register_user(token=token,
                                         username="TestUser",
                                         first_name="Watson",
                                         last_name="Christe",
                                         password="1234",
                                         email="jhu@gmail.com",
                                         is_temp_password=False)
    print(response)


# This will enable the user, after enabling user can login
def enable_user():
    response = user_client.enable_user(token=token,
                                       username="TestUser")
    print(response)


# Successfull login will return AccessToken, Id Token, and refresh token
def user_login():
    response = id_client.token(token=token, username="TestUser", password="1234", grant_type="password")
    print (response)


def reset_password():
    response = user_client.reset_password(token=token, username="TestUser", password="12345")
    print (response)


def get_decoding_secret():
    jwks = secret_client.get_JWKS(token=token)
    print (jwks)



get_decoding_secret()