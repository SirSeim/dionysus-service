from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

from addition import clients, enums, models
from addition.filters import AttributeFilter


class AdditionSerializer(serializers.Serializer):
    # read only fields
    id = serializers.CharField(read_only=True)
    state = serializers.ChoiceField(choices=enums.State, read_only=True)
    name = serializers.CharField(read_only=True)
    progress = serializers.FloatField(read_only=True)

    # write only fields
    magnet_link = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return clients.Transmission.add_torrent(validated_data["magnet_link"])


class AdditionListView(generics.ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = AdditionSerializer

    filter_backends = [OrderingFilter, AttributeFilter]
    ordering_fields = models.Addition.fields()
    ordering = "name"
    object_fields = models.Addition.fields()

    def get_queryset(self) -> models.ObjectSet[models.Addition]:
        return clients.Transmission.get_torrents() + clients.FileSystem.get_files()