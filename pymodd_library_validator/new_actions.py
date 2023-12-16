# auto generated


@action
def add_bot_player(name, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'addBotPlayer',
		'name': to_dict(name),
	}


@action
def hide_ui_element_for_player(element_id, player, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'hideUiElementForPlayer',
		'element_id': to_dict(element_id),
		'player': to_dict(player),
	}


@action
def show_ui_element_for_player(element_id, player, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'showUiElementForPlayer',
		'element_id': to_dict(element_id),
		'player': to_dict(player),
	}


@action
def set_ui_element_html(html_str, element_id, player, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'setUIElementHtml',
		'html_str': to_dict(html_str),
		'element_id': to_dict(element_id),
		'player': to_dict(player),
	}


@action
def append_realtime_css_for_player(value, player, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'appendRealtimeCSSForPlayer',
		'value': to_dict(value),
		'player': to_dict(player),
	}


@action
def update_realtime_css_for_player(value, player, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'updateRealtimeCSSForPlayer',
		'value': to_dict(value),
		'player': to_dict(player),
	}


@action
def stop_moving_unit(entity, comment=None, disabled=False, run_on_client=False):
	return {
		'type': 'stopMovingUnit',
		'entity': to_dict(entity),
	}