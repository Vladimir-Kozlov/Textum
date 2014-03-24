from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields

from textum.textedit.models import TImage


class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)


class TImageResource(MultipartResource, ModelResource):
    file = fields.FileField(attribute="file", null=True, blank=True)

    class Meta:
        always_return_data=True
        queryset = TImage.objects.all()
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        bundle.data["page_num"] = None
        return super(TImageResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, **kwargs):
        if bundle.data["page_num"] == '?':
            bundle.data["page_num"] = None
        return super(TImageResource, self).obj_update(bundle, **kwargs)

    def alter_detail_data_to_serialize(self, request, data):
        if data.data["page_num"] is None:
            data.data["page_num"] = '?'
        return data

    def alter_list_data_to_serialize(self, request, data):
        for bundle in data["objects"]:
            if bundle.data["page_num"] is None:
                bundle.data["page_num"] = '?'
        return data["objects"]