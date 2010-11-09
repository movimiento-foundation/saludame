# -*- coding: utf-8 -*-

import status_bars
from gettext import gettext as _

class BarsLoader:
    """
    This is just for create the bars, and not full
    of this static code the others class.
    """
    
    def __init__(self):
        hard_level = (100, 70)
        
        self.score_bar = status_bars.StatusBar("score_bar", _("Score"), None, [], 100, 0)
        self.overall_bar = status_bars.StatusBar("overall_bar", _("Overall"), None, [], 100, 70)
        
        #'hard_level' para plasmar que la idea es que los valores por defecto de las barras
        #se carguen segun un nivel de dificultad
        # physica
        physica_children_id = [("energy", _(u"Energía")), ("resistencia", _("Resistencia")), ("weight", _("Peso"))]
        physica = status_bars.StatusBar("physica", "Physica", self.overall_bar, [], hard_level[0], hard_level[1])
        physica_children_bar = [status_bars.StatusBar(id[0], id[1], physica, [], hard_level[0], hard_level[1]) for id in physica_children_id]
        physica.children_list = physica_children_bar
        
        ### hygiene
        hygiene_children_id = [("shower", _("Ducha")), ("w_hands", _("Manos")), ("b_teeth", _("Dientes")), ("toilet", _(u"Baño"))]
        hygiene = status_bars.StatusBar("hygiene", "Hygiene", self.overall_bar, [], hard_level[0], hard_level[1])
        hygiene_children_bar = [status_bars.StatusBar(id[0], id[1], hygiene, [], hard_level[0], hard_level[1]) for id in hygiene_children_id]
        hygiene.children_list = hygiene_children_bar

        ### nutrition 
        nutrition_children_id = [("c_leguminosas", _("Cereales y leguminosas")), ("v_frutas", _("Verduras y frutas")), ("c_huevos", _("Carnes y huevos")), ("dulces", _("Dulces")), ("g_aceites", _("Grasas y aceites")), ("l_quesos", _("Leches y quesos")), ("agua", _("Agua"))]
        nutrition = status_bars.StatusBar("nutrition", _("Nutrition"), self.overall_bar, [], hard_level[0], hard_level[1])
        nutrition_children_bar = [status_bars.StatusBar(id[0], id[1], nutrition, [], hard_level[0], hard_level[1]) for id in nutrition_children_id]
        nutrition.children_list = nutrition_children_bar
        
        ### fun 
        fun_children_id = [("sports", _("Deportes")), ("fun", _(u"Diversión")), ("relaxing", _("Descanso")), ("responsability", _("Responsabilidad"))]
        fun = status_bars.StatusBar("spare_time", _("Tiempo Libre"), self.overall_bar, [], hard_level[0], hard_level[1])
        fun_children_bar = [status_bars.StatusBar(id[0], id[1], fun, [], hard_level[0], hard_level[1]) for id in fun_children_id]
        fun.children_list = fun_children_bar
        
        self.second_level = [physica, hygiene, nutrition, fun]
        self.third_level = physica.children_list + hygiene.children_list + nutrition.children_list + fun.children_list
        
        self.overall_bar.children_list = self.second_level
        
        self.bars = self.second_level + self.third_level + [self.overall_bar] + [self.score_bar]
        
        self.bars_controller = status_bars.BarsController(self.bars, self.score_bar, self.overall_bar)
        
    def get_bar_controller(self):
        return self.bars_controller
    
    def get_second_level_bars(self):
        return self.second_level
    
    def get_third_level_bars(self):
        return self.third_level
    
    def get_overall_bar(self):
        return self.overall_bar
    
    def get_score_bar(self):
        return self.score_bar

