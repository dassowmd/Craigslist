from rest_framework import serializers
from models import Listing


class ListingSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
    view_name = 'listings-api:detail',
    lookup_field = 'pk')
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

class ListingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

