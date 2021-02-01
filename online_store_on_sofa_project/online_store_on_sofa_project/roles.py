from rolepermissions.roles import AbstractUserRole


class OperatorCallCenter(AbstractUserRole):
    available_permissions = {
        'feedback_with_clients': True,
    }


class ContentManager(AbstractUserRole):
    available_permissions = {
        'add_products': True,
        'add_images_for_product': True,
        'change_info_existing_products': True,
    }


class TopManager(AbstractUserRole):
    available_permissions = {
        'add_products': True,
        'feedback_with_clients': True,
        'add_images_for_product': True,
        'change_info_existing_products': True,
        'get_analytics': True,
    }

