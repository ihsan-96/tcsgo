from django.contrib import admin


from .models import Users

from .models import UsersAdmin

from .models import Points

from .models import Cars

from .models import Groups

from .models import GroupsAdmin

from .models import Requests

from .models import GroupsHistory


admin.site.register(Users, UsersAdmin)

admin.site.register(Points)

admin.site.register(Cars)

admin.site.register(Groups, GroupsAdmin)

admin.site.register(Requests)

admin.site.register(GroupsHistory)
