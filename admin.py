from django.contrib import admin
from django.contrib.postgres import fields

# import code for AJAX select
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# django_json_widget imports
from django_json_widget.widgets import JSONEditorWidget

# Import models
from context.models import Entity
from context.models import Entity_Identifier
from context.models import Entity_Identifier_Type
from context.models import Entity_Relation
from context.models import Entity_Relation_Trait
from context.models import Entity_Relation_Identifier
from context.models import Entity_Relation_Type
from context.models import Entity_Relation_Type_Trait
from context.models import Entity_Relation_Types
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
#admin.site.register( Entity )
#admin.site.register( Entity_Identifier )
#admin.site.register( Entity_Identifier_Type )
#admin.site.register( Entity_Relation )
admin.site.register( Entity_Relation_Identifier )
#admin.site.register( Entity_Relation_Type )
admin.site.register( Entity_Relation_Type_Trait )
#admin.site.register( Entity_Trait )
#admin.site.register( Entity_Type )
#admin.site.register( Entity_Type_Trait )
admin.site.register( Entity_Types )
#admin.site.register( Term )
admin.site.register( Term_Relation )
admin.site.register( Term_Relation_Type )
#admin.site.register( Trait_Type )
#admin.site.register( Vocabulary )
admin.site.register( Work_Log )


#==============================================================================#
# ! ==> Admins
#==============================================================================#


#-------------------------------------------------------------------------------
# ! --> Entity admin definition
#-------------------------------------------------------------------------------

# type inline
class Entity_EntityTypesInline( admin.TabularInline ):

    model = Entity_Types
    extra = 1
    fk_name = 'entity'

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'entity_type', 'tags' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class Entity_EntityTypesInline --#

# identifier inline
class Entity_EntityIdentifierInline( admin.TabularInline ):

    model = Entity_Identifier
    extra = 1
    fk_name = 'entity'
    
    fieldsets = [
        (
            None,
            {
                'fields' : [ 'id_type', 'name', 'uuid', 'source' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class Entity_EntityIdentifierInline --#

# trait inline
class Entity_EntityTraitInline( admin.TabularInline ):

    model = Entity_Trait
    extra = 1
    fk_name = 'entity'
    
    #formfield_overrides = {
    #    fields.JSONField: {'widget': JSONEditorWidget},
    #}
    
    fieldsets = [
        (
            None,
            {
                'fields' : [ 'name', 'value', 'value_json', 'label', 'tags', 'trait_type', 'term' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'description', 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class Entity_EntityTraitInline --#


class EntityAdmin( admin.ModelAdmin ):

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    
    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'name', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ "details_json", "notes" ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    inlines = [
        Entity_EntityTypesInline,
        Entity_EntityIdentifierInline,
        Entity_EntityTraitInline
    ]

    list_display = ( 'id', 'name', 'last_modified' )
    list_display_links = ( 'id', 'name' )
    #list_filter = [ 'location' ]
    search_fields = [ 'name', 'details_json', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'
    ordering = [ '-last_modified' ]

#-- END EntityAdmin admin model --#

admin.site.register( Entity, EntityAdmin )


#-------------------------------------------------------------------------------
# ! --> Entity_Identifier admin definition
#-------------------------------------------------------------------------------

class Entity_IdentifierAdmin( admin.ModelAdmin ):

    autocomplete_fields = [ 'entity', 'entity_identifier_type' ]

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'name', 'entity_identifier_type', 'entity', 'uuid', 'source', 'id_type' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ 'notes', 'tags' ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'name', 'entity_identifier_type', 'entity', 'uuid', 'source', 'last_modified' )
    list_display_links = ( 'id', 'name', 'entity_identifier_type' )
    list_filter = [ 'entity_identifier_type', 'source' ]
    search_fields = [ 'name', 'uuid', 'source', 'id_type', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'
    ordering = [ '-last_modified' ]

#-- END Entity_IdentifierAdmin admin model --#

admin.site.register( Entity_Identifier, Entity_IdentifierAdmin )


#-------------------------------------------------------------------------------
# ! --> Entity_Identifier_Type admin definition
#-------------------------------------------------------------------------------

class Entity_Identifier_TypeAdmin( admin.ModelAdmin ):

    autocomplete_fields = [ 'type_list' ]

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'name', 'label', 'source', 'type_list', 'tags', 'notes' ]
            },
        ),
    ]

    list_display = ( 'id', 'name', 'label', 'source', 'type_list_to_string', 'last_modified' )
    list_display_links = ( 'id', 'name', 'label' )
    list_filter = [ 'source' ]
    search_fields = [ 'name', 'label', 'source', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'
    ordering = [ '-last_modified' ]

#-- END Entity_TypeAdmin admin model --#

admin.site.register( Entity_Identifier_Type, Entity_Identifier_TypeAdmin )


#-------------------------------------------------------------------------------
# ! --> Entity_Relation admin definition
#-------------------------------------------------------------------------------

# type inline
class ER_EntityRelationTypesInline( admin.TabularInline ):

    model = Entity_Relation_Types
    extra = 1
    fk_name = 'entity_relation'

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'entity_relation_type', 'tags' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class ER_EntityRelationTypesInline --#

# identifier inline
class ER_EntityRelationIdentifierInline( admin.TabularInline ):

    model = Entity_Relation_Identifier
    extra = 1
    fk_name = 'entity_relation'
    
    fieldsets = [
        (
            None,
            {
                'fields' : [ 'id_type', 'name', 'uuid', 'source' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class Entity_EntityIdentifierInline --#

# trait inline
class ER_EntityRelationTraitInline( admin.TabularInline ):

    model = Entity_Relation_Trait
    extra = 1
    fk_name = 'entity_relation'
    
    fieldsets = [
        (
            None,
            {
                'fields' : [ 'name', 'value', 'label', 'tags', 'trait_type', 'term' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'description', 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class ER_EntityRelationTraitInline --#


class Entity_RelationAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Entity_Relation, dict( relation_from = 'entity', relation_to = 'entity', relation_through = 'entity' ) )
    autocomplete_fields = [ 'relation_from', 'relation_to', 'relation_through' ]

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    
    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'relation_from', 'relation_to', 'relation_through', 'directed', 'relation_type', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ "details_json", "notes" ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    inlines = [
        ER_EntityRelationTypesInline,
        ER_EntityRelationIdentifierInline,
        ER_EntityRelationTraitInline
    ]

    list_display = ( 'id', 'relation_type', 'relation_from', 'relation_to', 'last_modified' )
    list_display_links = ( 'id', 'relation_type' )
    #list_filter = [ 'location' ]
    search_fields = [ 'details_json', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'
    ordering = [ 'last_modified' ]

#-- END TermAdmin admin model --#

admin.site.register( Entity_Relation, Entity_RelationAdmin )


#-------------------------------------------------------------------------------
# ! --> Entity_Relation_Type admin definition
#-------------------------------------------------------------------------------

# type inline
class ERT_Entity_Relation_Type_TraitInline( admin.TabularInline ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Entity_Relation_Type_Trait, dict( trait_type = 'trait_type' ) )
    autocomplete_fields = [ 'trait_type' ]

    model = Entity_Relation_Type_Trait
    extra = 1
    fk_name = 'related_type'

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'slug', 'name', 'label', 'trait_type', 'required', 'tags' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class Entity_EntityTypesInline --#


class Entity_Relation_TypeAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Entity_Relation_Type, dict( parent_type = 'entity_relation_type', relation_from_entity_type = 'entity_type', relation_to_entity_type = 'entity_type' ) )
    autocomplete_fields = [ 'parent_type', 'relation_from_entity_type', 'relation_to_entity_type', 'relation_through_entity_type' ]

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'slug', 'name', 'description', 'tags', 'parent_type', 'relation_from_entity_type', 'relation_to_entity_type', 'relation_through_entity_type' ]
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

    inlines = [
        ERT_Entity_Relation_Type_TraitInline,
    ]

    list_display = ( 'id', 'slug', 'name', 'description', 'last_modified' )
    list_display_links = ( 'id', 'slug' )
    #list_filter = [ 'location' ]
    search_fields = [ 'slug', 'name', 'description', 'related_model', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'
    ordering = [ '-last_modified' ]

#-- END Entity_TypeAdmin admin model --#

admin.site.register( Entity_Relation_Type, Entity_Relation_TypeAdmin )


#-------------------------------------------------------------------------------
# ! --> Entity_Trait admin definition
#-------------------------------------------------------------------------------

# trait inline
class Entity_TraitAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Entity_Trait, dict( trait_type = 'trait_type', term = 'term' ) )
    autocomplete_fields = [ 'trait_type', 'term' ]

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    
    fieldsets = [
        (
            None,
            {
                'fields' : [ 'name', 'value', 'value_json', 'label', 'tags', 'trait_type', 'term' ]
            }
        ),
        (
            "More Detail (optional)",
            {
                'fields' : [ 'description', 'notes' ],
                'classes' : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'name', 'value', 'value_json', 'label', 'tags' )
    list_display_links = ( 'id', 'name' )
    #list_filter = [ 'location' ]
    search_fields = [ 'name', 'value', 'value_json', 'label', 'description', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'

#-- END class Entity_EntityTraitInline --#

admin.site.register( Entity_Trait, Entity_TraitAdmin )

#-------------------------------------------------------------------------------
# ! --> Entity_Type admin definition
#-------------------------------------------------------------------------------

# type inline
class ET_Entity_Type_TraitInline( admin.TabularInline ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Entity_Type_Trait, dict( trait_type = 'trait_type' ) )
    autocomplete_fields = [ 'trait_type' ]

    model = Entity_Type_Trait
    extra = 1
    fk_name = 'related_type'

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'slug', 'name', 'label', 'trait_type', 'required', 'tags' ]
            }
        ),
        #(
        #    "More Detail (optional)",
        #    {
        #        'fields' : [ 'notes' ],
        #        'classes' : ( "collapse", )
        #    }
        #),
    ]

#-- END class Entity_EntityTypesInline --#


class Entity_TypeAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Entity_Type, dict( parent_type = 'entity_type' ) )
    autocomplete_fields = [ 'parent_type' ]

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'slug', 'name', 'description', 'tags', 'parent_type' ]
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

    inlines = [
        ET_Entity_Type_TraitInline,
    ]

    list_display = ( 'id', 'slug', 'name', 'description', 'last_modified', 'create_date' )
    list_display_links = ( 'id', 'slug' )
    #list_filter = [ 'location' ]
    search_fields = [ 'slug', 'name', 'description', 'related_model', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'
    ordering = [ '-last_modified' ]

#-- END Entity_TypeAdmin admin model --#

admin.site.register( Entity_Type, Entity_TypeAdmin )


#-------------------------------------------------------------------------------
# ! --> Entity_Type_Trait admin definition
#-------------------------------------------------------------------------------


class Entity_Type_TraitAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Trait_Type, dict( vocabulary = 'vocabulary' ) )
    autocomplete_fields = [ 'trait_type', 'related_type' ]

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'slug', 'name', 'label', 'trait_type', 'related_type', 'required', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ 'description', 'notes' ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'slug', 'name', 'label', 'trait_type', 'related_type', 'required', 'last_modified' )
    list_display_links = ( 'id', 'slug', 'name', 'label' )
    list_filter = [ 'related_type', 'trait_type' ]
    search_fields = [ 'slug', 'name', 'label', 'trait_type', 'related_type', 'description', 'notes', 'id' ]
    date_hierarchy = 'last_modified'

#-- END TermAdmin admin model --#

admin.site.register( Entity_Type_Trait, Entity_Type_TraitAdmin )


#-------------------------------------------------------------------------------
# ! --> Term admin definition
#-------------------------------------------------------------------------------

class TermAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Term, dict( vocabulary = 'vocabulary' ) )
    autocomplete_fields = [ 'vocabulary' ]

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
# ! --> Trait_Type admin definition
#-------------------------------------------------------------------------------


class Trait_TypeAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Trait_Type, dict( vocabulary = 'vocabulary' ) )
    autocomplete_fields = [ 'vocabulary' ]

    fieldsets = [
        (
            None,
            { 
                'fields' : [ 'slug', 'name', 'vocabulary', 'tags' ]
            },
        ),
        (
            "More details (Optional)",
            {
                "fields" : [ 'description', 'related_model', 'notes' ],
                "classes" : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'slug', 'name', 'vocabulary' )
    list_display_links = ( 'id', 'slug' )
    #list_filter = [ 'location' ]
    search_fields = [ 'slug', 'name', 'related_model', 'description', 'notes', 'id' ]
    #date_hierarchy = 'pub_date'

#-- END TermAdmin admin model --#

admin.site.register( Trait_Type, Trait_TypeAdmin )


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
    #    in this case, implemented in context.lookups.py
    #form = make_ajax_form( Term, dict( parent_term = 'term' ) )
    autocomplete_fields = [ 'parent_term' ]

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

