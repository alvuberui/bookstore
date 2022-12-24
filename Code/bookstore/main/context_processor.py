from main.models import categorias, get_categorias_choices

def total_carrito(request):
    total = 0
    if "carrito" in request.session.keys():
        for key, value in request.session["carrito"].items():
            total += float(value["acumulado"])
    return {"total_carrito": total}


def categorias_lista(request):
    return {"categorias_list_all": get_categorias_choices()}
    


