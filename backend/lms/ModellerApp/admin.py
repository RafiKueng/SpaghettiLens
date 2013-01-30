'''
Created on 26.01.2013

@author: RafiK
'''

from ModellerApp.models import BasicLensData, ModellingResult, ModellingSession
from django.contrib import admin


class BasicLensDataAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'imgType']}),
        ('Channel Information', {'fields': ['channel1_data', 'channel1_imgurl', 'channel1_type',
                                            'channel2_data', 'channel2_imgurl', 'channel2_type',
                                            'channel3_data', 'channel3_imgurl', 'channel3_type']}),
    ]



#admin.site.register(BasicLensData, BasicLensDataAdmin)
admin.site.register(BasicLensData)
admin.site.register(ModellingResult)
admin.site.register(ModellingSession)
