import json

from django.utils import timezone
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from foodtaskerapp.models import Restaurent,Meals,Order,OrderDetails
from foodtaskerapp.serializers import RestaurentSerializer,MealSerializer,OrderSerializer

###############
#CUSTOMER     #
###############
def customer_get_restaurents(request):

    restaurents = RestaurentSerializer(
        Restaurent.objects.all().order_by("-id"),
        many = True,
        context = {"request": request }
    ).data

    return JsonResponse({"restaurents":restaurents})

def customer_get_meals(request,restaurent_id):

    meals = MealSerializer(
        Meals.objects.filter(restaurent_id = restaurent_id).order_by("-id"),
        many = True,
        context = {"request": request }
    ).data
    return JsonResponse({"meals": meals })

@csrf_exempt
def customer_add_orders(request):
    """
        parms:
            access_token
            restaurant_id
            address
            order_details(json format),example:
                [{ "meal_id":1, "quantity":2 },{ "meal_id":2, "quantity":3 }]
            stripe_token

        return:
            {"status": "success"}
    """
    if request.method == "POST":
        #GET token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt =timezone.now())

        #Get profile
        customer = access_token.user.customer

        #Check wheather customer has any order which is not delivered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({ "status": "failed", "error": "Your last order must be completed." })

        #Check address
        if not request.POST["address"]:
            return JsonResponse({ "status": "failed" , "error": "Address is required."})

        # Get order Order
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for meal in order_details:
            order_total += Meals.objects.get(id = meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:
            #Step 1 - create an order
            order = Order.objects.create(
                customer = customer,
                restaurent_id = request.POST["restaurent_id"],
                total = order_total,
                status = Order.COOKING,
                address = request.POST["address"]
            )


            #Step 2 - create order details
            for meal in order_details:
                OrderDetails.objects.create(
                    order = order,
                    meal_id = meal["meal_id"],
                    quantity = meal["quantity"],
                    sub_total = Meals.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                )
            return JsonResponse({"status": "success"})


def customer_get_latest_orders(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt= timezone.now())
    customer = access_token.user.customer
    order = OrderSerializer(
        Order.objects.filter(customer = customer).last()
    ).data
    return JsonResponse({"order": order})

###############
# RESTAURANT  #
###############

def restaurent_order_notification(request,last_request_time):
    notification = Order.objects.filter(restaurent = request.user.restaurent,
    created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})

###############
# DRIVERS     #
###############

def driver_get_ready_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(status = Order.READY, driver = None).order_by("-id"),
        many = True
    ).data
    return JsonResponse({ "orders": orders })

@csrf_exempt
# POST
#params: access_token,order_id
def driver_pick_orders(request):
    if request.method == "POST":
        # Get token
        access_token=AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

        # Get driver
        driver = access_token.user.driver

        #check if driver can pick up only one order at same time
        if Order.objects.filter(driver = driver).exclude(status = Order.ONTHEWAY):
            return JsonResponse({"status": "failed","error": "you can only one order at the same time" })

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                diver = None
                status = Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()
            return JsonResponse({"status":"success"})

        except Order.DoesNotExist:
            return JsonResponse({"status":"failed","error":"This order has been picked up by another driver "})

    return JsonResponse({})

def driver_get_latest__orders(request):
    return JsonResponse({})

def driver_complete_orders(request):
    return JsonResponse({})


def driver_get_revenue(request):
    return JsonResponse({})
