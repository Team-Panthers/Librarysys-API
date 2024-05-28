from django.core.cache import cache


class CacheManager:
    def __init__(self, model_class):
        self.model_class = model_class

    def generate_cache_key(self, custom_key=''):
        model_name = self.model_class.__name__.lower()
        if custom_key:
            return f"{model_name}_{custom_key}"
        return model_name

    def set_cache_data(self, data, custom_key='', timeout=900):
        cache_key = self.generate_cache_key(custom_key)
        cache.set(cache_key, data, timeout)

    def get_cache_data(self, custom_key=''):
        cache_key = self.generate_cache_key(custom_key)
        return cache.get(cache_key)

    def clear_cache_data(self, custom_key=''):
        cache_key = self.generate_cache_key(custom_key)
        cache.delete(cache_key)
