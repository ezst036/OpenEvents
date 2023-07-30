from django.shortcuts import get_object_or_404, render
import stripe
from checkout.models import StripeKeys
from . models import Event
from django.contrib import messages
from . forms import EventForm, AccountVerificationForm

from django.views.generic.base import TemplateView

class EventsHomeView(TemplateView):
    template_name = 'events/events.html'

    def get_context_data(self, **kwargs):
        try: #Always return the first available
            apikeys = StripeKeys.objects.all().first()
            if apikeys.stripepublic[:6] == "STRIPE" or apikeys.stripepublic[:6] == "STRIPE":
                 messages.success(self, f'API keys not yet setup by the administrator.')
        except Exception as e:
            #Deleted keys
            print(e)

        stripe.api_key = apikeys.stripesecret

        context = super().get_context_data(**kwargs)
        context['key'] = apikeys.stripepublic
        return context

def reviewConfirm(request):
   if request.method == "POST":
        #get item information
        event = Event.objects.get(id=request.POST['item_id'])

        try:
            apikeys = StripeKeys.objects.all().first()
        except Exception as e:
            print(e)

        stripe.api_key = apikeys.stripesecret

        if request.user.is_authenticated:
            #Display user's information
            userform = AccountVerificationForm(initial={
                        'email': request.user.email,
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'phone_number': request.user.phone_number,
                        'address': request.user.address,
                        'city': request.user.city,
                        'state': request.user.state,
                    })
            
            userform.fields['email'].disabled = True
        else:
            #blank form
            userform = AccountVerificationForm()
        
        #Event information
        payform = EventForm(initial={
                     'name': event.name,
                     'description': event.description,
                     'price': event.get_display_price
                 })
        
        payform.fields['name'].disabled = True
        payform.fields['description'].disabled = True
        payform.fields['price'].disabled = True
        
        return render(request, 'events/reviewevent.html', {'payform': payform,
                                                           "STRIPE_PUBLIC_KEY": apikeys.stripepublic,
                                                           'userform': userform,
                                                           'event':event})


        # amount = int(request.POST["amount"]) 

        # customer = stripe.Customer.create(
        #     email=request.POST.get("email"),
        #     name=request.POST.get("full_name"),
        #     description="item name",
        #     source=request.POST['stripeToken']
        # )

        # charge = stripe.Charge.create(
        #         customer=customer,
        #             amount=amount,
        #             currency='usd',
        #             description=""
        #         ) 
        # transRetrieve = stripe.Charge.retrieve(
        #             charge["id"],
        #             api_key="key"
        #         )
        # charge.save()
        #return redirect("pay_success/")
   


def chargeEvent(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount = request.POST['item_price'],
            currency='usd',
            description=request.POST['item_name'],
            source=request.POST['stripeToken'],
        )
        return render(request, 'events/charge.html')

def eventlist(request):
    event = Event.objects.filter(available=True)
    
    return render(request, 'events/listcontainer.html', {'events':event})

def eventdetail(request, id, slug):
    event=get_object_or_404(Event, id=id, slug=slug, available=True)

    event.price = event.price / 100
   
    return render(request, 'events/detail.html', {'product':event})
