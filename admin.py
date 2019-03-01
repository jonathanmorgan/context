from django.contrib import admin

# Import models
from context.models import Entity
from context.models import Entity_Relation
from context.models import Entity_Relation_Type
from context.models import Entity_Trait
from context.models import Entity_Trait_Type
from context.models import Entity_Type
from context.models import Entity_Types
from context.models import Term
from context.models import Term_Relation
from context.models import Term_Relation_Type
from context.models import Vocabulary
from context.models import Work_Log

# Register your models here.
admin.site.register( Entity )
admin.site.register( Entity_Relation )
admin.site.register( Entity_Relation_Type )
admin.site.register( Entity_Trait )
admin.site.register( Entity_Trait_Type )
admin.site.register( Entity_Type )
admin.site.register( Entity_Types )
admin.site.register( Term )
admin.site.register( Term_Relation )
admin.site.register( Term_Relation_Type )
admin.site.register( Vocabulary )
admin.site.register( Work_Log )
