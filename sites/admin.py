import logging
from django.contrib import admin
from django.contrib.auth.models import Group
from sites.models import About, Attributes, AuthToken, Organization, Project, Connection, Contact, Uniqueuser, AttributeGroup, GraphNode, NodeType, Key, Sysadmin, Room, get_or_add_authtoken, SSOObj
from sites.forms import ProjectAdminForm, SysadminAdminForm
from ssop import settings

logger = logging.getLogger('ssop.models')

 
def set_dbfield_to_sysad(fieldname, field, db_field, request):
    if fieldname in str(db_field):
        now = datetime.datetime.utcnow()
        #msg = str(now) + ':' + fieldname + ':' + str(db_field) + ":" + get_sysad(request)
        #logger.info(msg)
        sysadmin = Sysadmin.objects.filter(username=request.user)
        if sysadmin.count() > 0:
            field.initial = str(sysadmin[0])
    return field

    
class AboutAdmin(admin.ModelAdmin):
    list_display = ('version', 'updated_mst')
    list_display_links = list_display
    readonly_fields = ('version', 'updated_mst', 'requirements')


class AttributesAdmin(admin.ModelAdmin):
    #list_display = ('fingerprint', 'decodedfingerprint', 'clearattrs', 'attrs', 'decodedattrs', 'graph_node_id')
    list_display = ('fingerprint', 'decodedfingerprint', 'decodedattrs', 'attrs')
    list_display_links = list_display
    #readonly_fields = list_display


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'created', 'expires', 'accessed', 'days_until_accessed')
    list_display_links = list_display
    readonly_fields = list_display


class ConnectionAdmin(admin.ModelAdmin):
    #list_display = ('name', 'project', 'requestattrs', 'uniqueuser', 'userattrs', 'token', 'created', 'loggedout')
    list_display = ('name', 'project', 'uniqueuser', 'token', 'created', 'loggedout')
    list_display_links = list_display
    readonly_fields = ('name', 'project', 'uniqueuser', 'created', 'loggedout', 'attrsgroup', 'connection_state')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'lastname', 'organization', 'organizations_list', 'last_connected')
    list_display_links = list_display
    ordering = ('email', 'lastname', 'firstname', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if str(db_field) == 'sites.Contact.organization':
            qs = Organization.objects.filter(name=settings.NONE_NAME)
            kwargs['initial'] = qs[0]
        return super(ContactAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        form = super(ContactAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if str(db_field) == 'sites.Contact.organizations':
            qs = Organization.objects.all().order_by('name')
            kwargs['queryset'] = qs
            form.initial = {qs[0].id: True}
        if str(db_field) == 'sites.Contact.renewal_tokens':
            qs = AuthToken.objects.all().order_by('token')
            if qs.count() < int(1):
                qs = get_or_add_authtoken(settings.NONE_NAME)                
            kwargs['queryset'] = qs
            form.initial = {qs[0].id: True}
        return form

#class OrganizationNodeAdmin(admin.ModelAdmin):
#    #list_display = ('name', 'current_projects', 'contact', 'email', 'graph_node_id')
#    list_display = ( 'name', 'leaf' )
#    list_display_links = list_display


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'current_projects', 'users')
    list_display_links = list_display
    ordering = ('name',)


# ****** NOTE *******: class ProjectAdminForm exists in forms.py and it defines field_order (which does not contain all of the list_display fields)
class ProjectAdmin(admin.ModelAdmin):
    #list_display = ('name', 'organization', 'enabled', 'expiretokens', 'return_to', 'queryparam', 'error_redirect', 'display_order', 'state', 'decrypt_key', 'graph_node_id')
    list_display = ('name', 'verbose_name', 'organization', 'enabled', 'idp', 'expiretokens', 'pfishing_resistant', 'queryparam', 'return_to', 'error_redirect', 'contacts_url', 'owner', 'users', 'list_app_params', 'decrypt_key', 'state', 'logoimg', 'showlogobin', 'display_order', 'state', 'decrypt_key', 'updated')
    list_display_links = list_display
    #readonly_fields = ('state', 'updater') 
    ordering = ('display_order', 'organization', 'name')

    form = ProjectAdminForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        form = super(ProjectAdmin, self).form
        if str(db_field) == 'sites.Project.userlist':
            kwargs['queryset'] = Contact.objects.all().order_by('firstname')
            ncontact = Contact.objects.filter(email=settings.NONE_EMAIL)
            if ncontact.count() > int(0):
                ncontact = ncontact[0]
                form = super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
                form.initial = {ncontact.id: True}
        if str(db_field) == 'sites.Project.groups':
            #kwargs['queryset'] = Group.objects.all().order_by('firstname')
            kwargs['queryset'] = Group.objects.all()
            #ncontact = Contact.objects.filter(email=settings.NONE_EMAIL)
            #if ncontact.count() > int(0):
            #    ncontact = ncontact[0]
            #    form = super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            #    form.initial = {ncontact.id: True}
            form = super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            form.initial = {0: True}
        return form


class SysadminAdmin(admin.ModelAdmin):
    list_display = ('username', 'organization', 'organizations_list')
    list_display_links = list_display
    form = SysadminAdminForm
                
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super(SysadminAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)
        field = set_dbfield_to_sysad('provision.Sysadmin.updater', field, db_field, request)
        return field


class UniqueuserAdmin(admin.ModelAdmin):
    #list_display = ('name', 'fingerprint', 'clearnameattrs', 'clearallattrs', 'clearconnattrs', 'attributes', 'connattributes', 'graph_node_id')
    list_display = ('name', 'fingerprint', 'clearnameattrs', 'clearallattrs', 'clearconnattrs', 'attributes', 'connattributes')
    list_display_links = list_display
    # readonly_fields = list_display


class AttributeGroupAdmin(admin.ModelAdmin):
    #list_display = ('name', 'attributes', 'graph_node_id')
    list_display = ('name', 'grouptype', 'clearattrs', 'attributes')
    list_display_links = list_display
    readonly_fields = list_display


class GraphNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'projectname', 'nodeid', 'node_type')
    list_display_links = list_display
    #readonly_fields = list_display


class NodeTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'attrs', 'options')
    list_display_links = list_display

class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'current_state', 'mode')
    list_display_links = list_display


admin.site.register(About, AboutAdmin)
admin.site.register(Attributes, AttributesAdmin)
admin.site.register(AttributeGroup, AttributeGroupAdmin)
admin.site.register(AuthToken, AuthTokenAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(GraphNode, GraphNodeAdmin)
admin.site.register(Key)
#admin.site.register(OrganizationNode, OrganizationNodeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(NodeType, NodeTypeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Sysadmin, SysadminAdmin)
admin.site.register(Uniqueuser, UniqueuserAdmin)
admin.site.register(SSOObj)
