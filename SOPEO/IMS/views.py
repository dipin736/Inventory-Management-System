from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory,Transaction,Orders
from .forms import InventoryForm,SellItemForm,CreateOrderForm
from django.db.models import Sum
import json

# Create your views here.

def management(request):
    try:
        with open('media/management.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    jsonData = json.dumps(data)
    context = {'jsonData': jsonData}
    context.update(data)
    return render(request, 'management.html', context)

def home(request):
    total_profit = Inventory.objects.aggregate(Sum('profit_earned'))['profit_earned__sum']
    total_items_in_stock = Inventory.objects.aggregate(Sum('quantity'))['quantity__sum']
    highest_cost_item = Inventory.objects.order_by('-cost').first()
    highest_profit_item = Inventory.objects.order_by('-profit_earned').first()
    most_sold_item = Inventory.objects.order_by('-quantity_sold').first()
    items_out_of_stock = Inventory.objects.filter(quantity=0)
    highest_profit_earned_item = Inventory.objects.order_by('-profit_earned').first()


    context = {
        'total_profit': total_profit,
        'total_items_in_stock': total_items_in_stock,
        'highest_cost_item': highest_cost_item,
        'highest_profit_item': highest_profit_item,
        'most_sold_item': most_sold_item,
        'items_out_of_stock': items_out_of_stock,
        'highest_profit_earned_item': highest_profit_earned_item,
    }

    return render(request, 'home.html', context)


def nav(request):
    return render(request, 'navbar/navbar.html')

def footer(request):
    return render(request, 'footer/footer.html')


# ......................inventory.........................  
# def create_inventory(request):
#     context = {}
#     if request.method == 'POST':
#         form = InventoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list_inventory')
#     else:
#         form = InventoryForm()
    
#     context['form'] = form  
#     return render(request, 'item/create.html', context)

def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_inventory')
    else:
        form = InventoryForm()
        context={'form': form } 
    return render(request, 'item/create.html', context)


def edit_inventory(request,item_id):
    inventory_item = get_object_or_404(Inventory, pk=item_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('list_inventory')
    else:
        form = InventoryForm(instance=inventory_item)
        context={
            'form':form
        }
    return render(request, 'item/edit.html',context)

def list_inventory(request):
    inventory_items = Inventory.objects.all()
    context={
        'inventory_items':inventory_items
    }
    return render(request, 'item/list.html',context)


def inventory_detail(request, item_id):
    inventory_item = get_object_or_404(Inventory, pk=item_id)
    related_orders = Orders.objects.filter(item=inventory_item)
    related_transactions = Transaction.objects.filter(item=inventory_item)
    context={
        'inventory_item':inventory_item,
        'related_orders': related_orders,
        'related_transactions': related_transactions,
    }
    return render(request, 'item/detail.html', context)


def delete_inventory(request,id):
    inventory_item = Inventory.objects.get(id=id)
    inventory_item.delete()
    return redirect('list_inventory')


# .................order.............................

def create_order(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.item = item
            order.cost = item.cost
            order.save()
            return redirect('list_orders') 
    else:
        form = CreateOrderForm()

    return render(request, 'order/create_order.html', {'item': item, 'form': form})

def list_orders(request):
    orders = Orders.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'item/list_order.html', context)

def confirm_order(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if not order.is_received and not order.is_cancel:
        order.is_received = True
        order.save()
        item = order.item
        item.quantity += order.quantity
        item.save()
    return redirect('list_orders')  

def cancel_order(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if not order.is_received and not order.is_cancel:
        order.is_cancel = True
        order.save()
    return redirect('list_orders')  


def orders_placed(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    orders = Orders.objects.filter(item=item)
    return render(request, 'order/orders_placed.html', {'item': item, 'orders': orders})

def orders_received(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    orders = Orders.objects.filter(item=item, is_received=True)
    return render(request, 'order/orders_received.html', {'item': item, 'orders': orders})

def orders_canceled(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    orders = Orders.objects.filter(item=item, is_cancel=True)
    return render(request, 'order/orders_canceled.html', {'item': item, 'orders': orders})


# .......................Transaction.............................

def sell_item(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    if request.method == 'POST':
        form = SellItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if item.quantity >= quantity:
                Transaction.objects.create(item=item, quantity=quantity, selling_price=item.selling_price * quantity)
                item.quantity -= quantity
                item.quantity_sold += quantity
                item.save()
                return redirect('inventory_detail',  item_id=item_id)
            else:
                form.add_error('quantity', 'Insufficient stock.')
    else:
        form = SellItemForm()

    return render(request, 'item/sell_item.html', {'item': item, 'form': form})


def items_sold(request, item_id):
    item = Inventory.objects.get(pk=item_id)
    transactions = Transaction.objects.filter(item=item)
    return render(request, 'order/items_sold.html', {'item': item, 'transactions': transactions})


def list_sold(request):
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions
    }
    return render(request, 'item/list_sold.html', context)

