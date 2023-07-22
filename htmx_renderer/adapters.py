from drf_auto_endpoint.adapters import EmberAdapter


class HTMXEndpointAdapter(EmberAdapter):

    @classmethod
    def adapt_field(cls, field):
        rv = super().adapt_field(field)

        if 'related_endpoint' in field:
            rv['extra']['related_endpoint'] = field['related_endpoint']

        return rv
