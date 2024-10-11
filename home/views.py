from django.shortcuts import render
from product.models import Product
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from account.models import Order,Profile,Cart,cartItems,ColorVariant,SizeVariant
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# Create your views here.

def check_color_variant(product_name, color):
    try:
        # Find the product by name
        product = Product.objects.get(product_name__iexact=product_name)
        
        # Check if the color exists in the product's color variants
        if product.color_variant.filter(color__iexact=color).exists():
            return True, product
        else:
            return False, None
    except Product.DoesNotExist:
        return False, None


def home_page(request):
    
    context={'products': Product.objects.all()}
    return render(request,"home/index.html",context)

def search_page(request):
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(product_desc__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        products = Product.objects.none()

    return render(request, 'home/search.html', {'products': products, 'query': query})

def add_to_cart_bot(user_profile, product_name, color_variant, quantity):
    try:
        # Case-insensitive matching for product name
        product = Product.objects.get(product_name__iexact=product_name)
        cart, _ = Cart.objects.get_or_create(user=user_profile, is_paid=False)

        cart_item = cartItems.objects.create(cart=cart, product=product, quantity=quantity)

        # Handle the color variant with case-insensitive matching
        if color_variant:
            color = ColorVariant.objects.get(color__iexact=color_variant)
            cart_item.color_variant = color
        else:
            return "Please select a color."

        cart_item.save()
        return f"{quantity} {product_name}(s) in {color_variant} added to your cart! How can I further assist you? You can say 'New order' or 'Track order'."
    except Product.DoesNotExist:
        return "The product does not exist."
    except ColorVariant.DoesNotExist:
        return "The selected color is not available."
    except Exception as e:
        return str(e)


@csrf_exempt
def handle_request(request):
    if request.method == "POST":
        # Parse the JSON request from Dialogflow
        try:
            data = json.loads(request.body)
            intent_name = data.get('queryResult', {}).get('intent', {}).get('displayName', None)
        except json.JSONDecodeError:
            return JsonResponse({"fulfillmentText": "Could not process the request."})

        # Handle the "track order:ongoing" intent
        if intent_name == "track order:ongoing":
            order_id = data.get('queryResult', {}).get('parameters', {}).get('order_id', None)
            
            if order_id:
                try:
                    # Find the order by order_id
                    order = Order.objects.get(order_id=order_id)
                    # Check the status of the order
                    status = order.status

                    # Return the status to the user
                    if status == "Delivered":
                        return JsonResponse({"fulfillmentText": f"Your order {order_id} has been delivered."})
                    elif status == "Processing":
                        return JsonResponse({"fulfillmentText": f"Your order {order_id} is currently being processed."})
                    else:
                        return JsonResponse({"fulfillmentText": f"Your order {order_id} is in {status} state."})

                except Order.DoesNotExist:
                    # If the order_id is not found
                    return JsonResponse({"fulfillmentText": f"Order with ID {order_id} does not exist."})
            else:
                return JsonResponse({"fulfillmentText": "Order ID not provided."})
            
        elif intent_name == "search.add-order":
            product_name = data.get('queryResult', {}).get('parameters', {}).get('product', None)
            
            if product_name:
                # Search for products in the database
                products = Product.objects.filter(
                    Q(product_name__icontains=product_name) |
                    Q(category__category_name__icontains=product_name)
                )

                product_count = products.count()
                session_path = data.get('session', '')
                project_id = session_path.split('/')[1]
                session_id = session_path.split('/')[4]

                # If multiple products are found, prompt the user to be more specific
                if product_count > 1:
                    product_names = ", ".join([product.product_name for product in products])
                    return JsonResponse({
                        "fulfillmentText": f"Multiple products found: {product_names}. Can you be more specific?"
                    })

                # If one product is found, proceed to ask for color and quantity
                elif product_count == 1:
                    product = products.first()
                    # Change the context to 'ongoing-add-order'
                    return JsonResponse({
                        "fulfillmentText": f"{product.product_name} found. What color and quantity would you like?",
                        "outputContexts": [
                            {
                                # Set the new context ongoing-add-order
                                "name": f"projects/{project_id}/agent/sessions/{session_id}/contexts/ongoing-add-order",
                                "lifespanCount": 5,
                                "parameters": {
                                    "product_name": product.product_name
                                }
                            },
                            {
                                # Remove the ongoing-new-order context by setting lifespanCount to 0
                                "name": f"projects/{project_id}/agent/sessions/{session_id}/contexts/ongoing-new-order",
                                "lifespanCount": 0
                            }
                        ]
                    })



                else:
                    return JsonResponse({"fulfillmentText": f"Sorry, no product found for {product_name}."})
            else:
                return JsonResponse({"fulfillmentText": "Please specify what you want to order."})

        if intent_name == "new-order:color-quantity":
            color = data.get('queryResult', {}).get('parameters', {}).get('color', None)
            quantity = data.get('queryResult', {}).get('parameters', {}).get('quantity', None)
            product_name = data.get('queryResult', {}).get('outputContexts', [{}])[0].get('parameters', {}).get('product_name', None)

            # Check if the quantity is provided and is not empty
            if not (product_name and color and quantity):
                return JsonResponse({"fulfillmentText": "Please specify the product color along with the quantity you want to add to the cart."})

            # Convert quantity to an integer only if it exists
            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                return JsonResponse({"fulfillmentText": "Please specify a valid quantity."})

            color_exists, product = check_color_variant(product_name, color)

            session_path = data.get('session', '')
            project_id = session_path.split('/')[1]
            session_id = session_path.split('/')[4]

            if color_exists:
                # Color is available, save details in the new context
                return JsonResponse({
                    "fulfillmentText": f"To add {quantity} {product_name}(s) of color {color}, you first need to provide your email.",
                    "outputContexts": [
                        {
                            # Create a new context ongoing-order-email
                            "name": f"projects/{project_id}/agent/sessions/{session_id}/contexts/ongoing-order-email",
                            "lifespanCount": 5,
                            "parameters": {
                                "product_name": product_name,
                                "color": color,
                                "quantity": quantity
                            }
                        },
                        {
                            # Remove the ongoing-add-order context by setting lifespanCount to 0
                            "name": f"projects/{project_id}/agent/sessions/{session_id}/contexts/ongoing-add-order",
                            "lifespanCount": 0
                        }
                    ]
                })
            else:
                # Color not available
                return JsonResponse({"fulfillmentText": f"Sorry, {color} is not available for {product_name}."})
        
        elif intent_name == "new-order:email":
            email = data.get('queryResult', {}).get('parameters', {}).get('email', None)
            output_contexts = data.get('queryResult', {}).get('outputContexts', [{}])
            context_params = output_contexts[0].get('parameters', {})

            session_path = data.get('session', '')
            project_id = session_path.split('/')[1]
            session_id = session_path.split('/')[4]

            product_name = context_params.get('product_name', None)
            color = context_params.get('color', None)
            quantity = context_params.get('quantity', None)

            if email and product_name and color and quantity:
                try:
                    # Find the user profile using the email
                    user_profile = Profile.objects.get(user__email=email)

                    # Add the product to the cart (this logic should already be in your code)
                    result = add_to_cart_bot(user_profile, product_name, color, quantity)

                    return JsonResponse({
                        "fulfillmentText": result,
                        "outputContexts": [
                        {
                            # Create a new context ongoing-order-email
                            "name": f"projects/{project_id}/agent/sessions/{session_id}/contexts/ongoing-order-email",
                            "lifespanCount": 0
                               
                        },]
                    })

                except Profile.DoesNotExist:
                    return JsonResponse({"fulfillmentText": "We could not find a user with that email. Please try again."})
            else:
                return JsonResponse({"fulfillmentText": "Please provide a valid email address."})
        
        else:
            return JsonResponse({"fulfillmentText": "Intent not recognized."})

    return JsonResponse({"fulfillmentText": "Invalid request method."})




