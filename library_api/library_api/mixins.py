class UserContextMixin():

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context