import logging

logger = logging.getLogger('django')


class Device:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if "Mobile" in user_agent:
            logger.info('Пользователь зашел с мобильного устройства')
        else:
            logger.info('Пользователь зашел с ПК')

        return response
