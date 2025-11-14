from django import template
from django.template import Context
from django.utils.safestring import mark_safe
from menu_app.models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Template tag для отрисовки меню.
    Использует только 1 запрос к БД благодаря select_related и prefetch_related.
    """
    try:
        # Получаем текущий URL из контекста
        request = context.get('request')
        current_url = request.path if request else ''
        
        # Один запрос к БД для получения всех пунктов меню
        menu_items = MenuItem.objects.filter(
            menu__name=menu_name
        ).select_related('parent', 'menu').order_by('order', 'id')
        
        if not menu_items.exists():
            return {'menu_items': []}
        
        # Строим структуру меню в памяти
        menu_dict = {}
        root_items = []
        
        # Первый проход: создаем словарь всех элементов
        for item in menu_items:
            menu_dict[item.id] = {
                'item': item,
                'children': [],
                'is_active': False,
                'is_expanded': False,
                'url': item.get_url()
            }
        
        # Второй проход: строим иерархию
        for item in menu_items:
            item_data = menu_dict[item.id]
            # Проверяем, является ли пункт активным
            item_data['is_active'] = (item_data['url'] == current_url)
            
            if item.parent_id:
                if item.parent_id in menu_dict:
                    menu_dict[item.parent_id]['children'].append(item_data)
            else:
                root_items.append(item_data)
        
        # Определяем, какие пункты должны быть развернуты
        def mark_expanded_items(items, parent_active=False):
            for item_data in items:
                children = item_data['children']
                
                # Проверяем, есть ли активные дети
                has_active_child = any(
                    mark_expanded_items([child], item_data['is_active'])[0]
                    for child in children
                )
                
                # Разворачиваем пункт если:
                # 1. Он сам активный
                # 2. У него есть активный потомок
                # 3. Его родитель активный (первый уровень под активным)
                if item_data['is_active'] or has_active_child or parent_active:
                    item_data['is_expanded'] = True
                
                # Возвращаем True, если элемент или его потомок активный
                return item_data['is_active'] or has_active_child
            
            return False
        
        # Отмечаем развернутые элементы
        for item in root_items:
            mark_expanded_items([item])
        
        return {
            'menu_items': root_items,
            'current_url': current_url
        }
        
    except Menu.DoesNotExist:
        return {'menu_items': []}