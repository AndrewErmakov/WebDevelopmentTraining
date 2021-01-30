from rolepermissions.roles import AbstractUserRole


class OperatorCallCenter(AbstractUserRole):
    available_permissions = {
        'feedback_with_clients': True,
    }


class ContentManager(AbstractUserRole):
    available_permissions = {
        'add_products': True,
    }


class TopManager(AbstractUserRole):
    available_permissions = {
        'add_products': True,
        'feedback_with_clients': True,
    }

