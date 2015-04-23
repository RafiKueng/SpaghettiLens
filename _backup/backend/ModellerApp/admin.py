'''
Created on 26.01.2013

@author: RafiK
'''

from ModellerApp.models import LensData, BasicLensData, ModellingResult, ModellingSession, Catalog
from django.contrib import admin


class BasicLensDataAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['name', 'catalog', 'catalog_img_id', 'img_type', 'z_lens', 'z_source']}),
        ('Administrative',      {'fields': ['n_res', 'requested_last']}),
        ('Channel Information', {'classes': ['collapse'],
                                 'fields': [('channel1_data', 'channel1_imgurl', 'channel1_type'),
                                            ('channel2_data', 'channel2_imgurl', 'channel2_type'),
                                            ('channel3_data', 'channel3_imgurl', 'channel3_type'),
                                            ('channel4_data', 'channel4_imgurl', 'channel4_type'),
                                            ('channel5_data', 'channel5_imgurl', 'channel5_type')]}),
    ]



admin.site.register(LensData)
admin.site.register(BasicLensData, BasicLensDataAdmin)
admin.site.register(Catalog)
admin.site.register(ModellingResult)
admin.site.register(ModellingSession)
