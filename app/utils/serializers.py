class CurrentUrlObject:
    requires_context = True

    def __init__(self, model, param_name="pk"):
        self.model = model
        self.param_name = param_name

    def __call__(self, serializer_field):
        return self.model.objects.get(**{"pk": serializer_field.context["view"].kwargs.get(self.param_name)})
