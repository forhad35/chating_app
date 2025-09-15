from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'  # Default হলো 'Token', এখন আমরা 'Bearer' set করছি
