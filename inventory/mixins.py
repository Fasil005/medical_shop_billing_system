class CreatedByMixin:
    """
    Mixin to automatically set `created_by` as `request.user`
    when creating or updating an object.
    """
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)