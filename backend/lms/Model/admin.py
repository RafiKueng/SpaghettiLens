'''
Created on 26.01.2013

@author: RafiK
'''

from Model.models import ModelData
from Model.models import Result
from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'imgType']}),
        ('Channel Information', {'fields': ['channel1_data', 'channel1_imgurl', 'channel1_type',
                                            'channel2_data', 'channel2_imgurl', 'channel2_type',
                                            'channel3_data', 'channel3_imgurl', 'channel3_type']}),
    ]

admin.site.register(ModelData, ModelAdmin)

admin.site.register(Result)
