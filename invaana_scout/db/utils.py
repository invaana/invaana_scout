

def get_or_create(Klass, *args, **kwargs):
    try:
        return True, Klass.objects.get(*args, **kwargs)
    except:
        return False, Klass.objects.create(*args, **kwargs)
