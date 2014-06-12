from rest_framework import permissions


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Define si se tiene permiso para realizar la accion
        :param request: objeto request
        :param view: vista desde donde se ejecuta la accion
        :return: boolean
        """
        # importamos aqui por que sino da problemas con otros imports
        from api import UserDetailAPI

        if request.method == "POST":
            return True

        # si es superuser, puede hacer un GET, PUT y DELETE si quiere
        elif request.user.is_superuser:
            return True

        # si no es superuser le dejamos acceder solo al detalle
        elif isinstance(view, UserDetailAPI):
            return True

        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Este metodo solo se ejecuta cuando se hace un PUT o DELETE
        sobre un objeto.
        Define si se tiene permiso para hacer PUT o DELETE.
        Solo tiene permiso si es propietario o es superuser
        :param request: objeto request
        :param view: vista desde donde se ejecuta
        :param obj: objeto sobre el que se ejecuta
        :return: boolean
        """
        if request.user.is_superuser or obj.owner == request.user:
            return True
        else:
            return False