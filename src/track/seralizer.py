from rest_framework import serializers


class EventSerializers(serializers.Serializer):
    n = serializers.CharField()  # event type
    u = serializers.CharField()  # users current url
    d = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # domain name with event
    r = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # referer url
    m = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # additional metadata
    p = serializers.DictField(required=False,allow_empty=True,)  # additional properties as object
