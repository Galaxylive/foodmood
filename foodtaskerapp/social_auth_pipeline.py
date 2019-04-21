
from foodtaskerapp.models import Driver,Customer


def create_user_by_type(backend, user,request,response, *args, **kwargs):
    if backend.name == 'facebook':
        avatar = 'https://graph.facebook.com/%s/picture?type=large' % response['id']
    #it will check if the user type is driver then it will check wheatherthe user is present in database or not
    if request['user_type'] == "driver" and not Driver.objects.filter(user_id = user.id):
        Driver.objects.create(user_id = user.id, avatar = avatar)
    elif not Customer.objects.filter(user_id = user.id):
        Customer.objects.create(user_id = user.id,avatar = avatar)
