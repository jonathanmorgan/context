from django.contrib import admin

# import code for AJAX select
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Import models
from context.models import Entity
from context.models import Entity_Relation
from context.models import Entity_Relation_Type
from context.models import Entity_Relation_Type_Trait
from context.models import Entity_Trait
from context.models import Entity_Type
from context.models import Entity_Type_Trait
from context.models import Entity_Types
from context.models import Term
from context.models import Term_Relation
from context.models import Term_Relation_Type
from context.models import Trait_Type
from context.models import Vocabulary
from context.models import Work_Log

# Register your models here.
admin.site.register( Entity )
admin.site.register( Entity_Relation )
admin.site.register( Entity_Relation_Type )
admin.site.register( Entity_Relation_Type_Trait )
admin.site.register( Entity_Trait )
#admin.site.register( Entity_Type )
admin.site.register( Entity_Type_Trait )
admin.site.register( Entity_Types )
#admin.site.register( Term )
admin.site.register( Term_Relation )
admin.site.register( Term_Relation_Type )
admin.site.register( Trait_Type )
#admin.site.register( Vocabulary )
admin.site.register( Work_Log )


#==============================================================================#
# ! ==> Admins
#==============================================================================#


#-------------------------------------------------------------------------------
# ! --> Entity_Type admin definition
#-------------------------------------------------------------------------------

class Entity_TypeAdmin( admin.ModelAdmin ):

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'slug', 'name', 'description', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ "related_model", "notes" ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'slug', 'name', 'description' )
    list_display_links = ( 'id', 'slug' )
    #list_filter = [ 'location' ]
    search_fields = [ 'slug', 'name', 'description', 'related_model', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'

#-- END Entity_TypeAdmin admin model --#

admin.site.register( Entity_Type, Entity_TypeAdmin )


#-------------------------------------------------------------------------------
# ! --> Term admin definition
#-------------------------------------------------------------------------------

class TermAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in sourcenet.ajax-select-lookups.py
    form = make_ajax_form( Term, dict( vocabulary = 'vocabulary' ) )

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'vocabulary', 'value', 'label', 'description', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ 'parent_term', 'notes' ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'value', 'label', 'vocabulary' )
    list_display_links = ( 'id', 'value' )
    #list_filter = [ 'location' ]
    search_fields = [ 'value', 'label', 'description', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'

#-- END TermAdmin admin model --#

admin.site.register( Term, TermAdmin )


#-------------------------------------------------------------------------------
# ! --> Vocabulary admin definition
#-------------------------------------------------------------------------------


#class TermInline( admin.StackedInline ):
class TermInline( admin.TabularInline ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in sourcenet.ajax-select-lookups.py
    form = make_ajax_form( Term, dict( parent_term = 'term' ) )

    model = Term
    extra = 2
    fk_name = 'vocabulary'
    
    fieldsets = [
        (
            None,
            {
                'fields' : [ 'value', 'label', 'tags' ]
            }
        ),
        (
            "More Detail (optional)",
            {
                'fields' : [ 'parent_term', 'description', 'notes' ],
                'classes' : ( "collapse", )
            }
        ),
    ]

#-- END class TermInline --#


class VocabularyAdmin( admin.ModelAdmin ):

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'name', 'description', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ "notes" ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    inlines = [
        TermInline,
    ]

    list_display = ( 'id', 'name', 'description' )
    list_display_links = ( 'id', 'name', )
    #list_filter = [ 'location' ]
    search_fields = [ 'name', 'description', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'

#-- END VocabularyAdmin admin model --#

admin.site.register( Vocabulary, VocabularyAdmin )

