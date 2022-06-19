from cgitb import reset
from skyrim.data.models import Battle
from django.shortcuts import render
from skyrim.domain.race.queries import get_all_races
from skyrim.domain.user.queries import get_all_users
from skyrim.domain.character.queries import get_character_from_place

# if(context['page_obj'].has_previous()):
#             self.request.GET = self.request.GET.copy()
#             self.request.GET['page'] = context['page_obj'].previous_page_number()
#             context['previous_url'] = self.request.GET.urlencode()

#         if(context['page_obj'].has_next()):
#             self.request.GET = self.request.GET.copy()
#             self.request.GET['page'] = context['page_obj'].next_page_number()
#             context['next_url'] = self.request.GET.urlencode()


def select_character_view(request, battle_id):
    battle = Battle.objects.get(id = battle_id)
    query = {}
    query['place_id'] = battle.place.id

    for key in request.GET.dict().keys():
        query[key] = request.GET.getlist(key,None)

    context = {}
    context['users_list'] = get_all_users()
    context['races_list'] = get_all_races()
    result = get_character_from_place(query,2) 
    context['character_list'] = result[1:]

    context['pagination'] = result[0]
    value = query.get('page',None)
    if(value == None):
        value = 1
    else:
        value = int(value[0])
    current_url = request.GET.copy()
    current_url['page'] = value - 1
    context['pagination']['previous_url'] = '?' + current_url.urlencode()
    current_url['page'] = value + 1
    context['pagination']['next_url'] = '?' + current_url.urlencode()

    return render(request, "select_character.html",context)
    