# -*- coding: utf-8 -*-

# Copyright (C) 2011 ceibalJAM! - ceibaljam.org
# This file is part of Saludame.
#
# Saludame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Saludame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Saludame. If not, see <http://www.gnu.org/licenses/>.

import status_bars
from gettext import gettext as _

class BarsLoader:
    """
    This is just for create the bars, and not full
    of this static code the others class.
    """
    
    def __init__(self):
        max_points = 100
        init_points = 50
        
        self.score_bar = status_bars.StatusBar("score_bar", _("Score"), None, [], 100, 0)
        self.overall_bar = status_bars.StatusBar("overall_bar", _("Overall"), None, [], max_points, init_points)
        
        #'hard_level' para plasmar que la idea es que los valores por defecto de las barras
        #se carguen segun un nivel de dificultad
        # physica
        physica_children_id = [("energy", _(u"Energía")), ("defenses", _("Defenses"))]
        physica = status_bars.StatusBar("physica", _("Physica"), self.overall_bar, [], max_points, init_points)
        physica_children_bar = [status_bars.StatusBar(id[0], id[1], physica, [], max_points, init_points) for id in physica_children_id]
        weight_bar = status_bars.WeightBar("weight", _("Peso"), physica, [], max_points, init_points)
        physica_children_bar.append(weight_bar)
        physica.children_list = physica_children_bar
        
        ### hygiene
        hygiene_children_id = [("shower", _("Shower")), ("w_hands", _("Wash Hands")), ("b_teeth", _("Brush Teeth")), ("toilet", _(u"Toilet"))]
        hygiene = status_bars.StatusBar("hygiene", _("Hygiene"), self.overall_bar, [], max_points, init_points)
        hygiene_children_bar = [status_bars.StatusBar(id[0], id[1], hygiene, [], max_points, init_points) for id in hygiene_children_id]
        hygiene.children_list = hygiene_children_bar

        ### nutrition
        nutrition_children_id = [("c_leguminosas", _("Cereales y leguminosas")), ("v_frutas", _("Verduras y frutas")), ("c_huevos", _("Carnes y huevos")), ("dulces", _("Dulces")), ("g_aceites", _("Grasas y aceites")), ("l_quesos", _("Leches y quesos")), ("agua", _("Agua"))]
        nutrition = status_bars.StatusBar("nutrition", _("Alimentation"), self.overall_bar, [], max_points, init_points)
        nutrition_children_bar = [status_bars.StatusBar(id[0], id[1], nutrition, [], max_points, init_points) for id in nutrition_children_id]
        nutrition.children_list = nutrition_children_bar
        
        ### spare time
        fun_children_id = [("sports", _("Sports")), ("fun", _(u"Fun")), ("relaxing", _("Rest"))]
        fun = status_bars.StatusBar("spare_time", _("Tiempo Libre"), self.overall_bar, [], max_points, init_points)
        fun_children_bar = [status_bars.StatusBar(id[0], id[1], fun, [], max_points, init_points) for id in fun_children_id]
        fun.children_list = fun_children_bar

        ### responsability
        resp_children_id = [("homework", _(u"Homework")), ("housekeeping", _("Housekeeping")), ("h_check", _("Health Check"))]
        resp = status_bars.StatusBar("responsability", _("Responsabilidad"), self.overall_bar, [], max_points, init_points)
        resp_children_bar = [status_bars.StatusBar(id[0], id[1], fun, [], max_points, init_points) for id in resp_children_id]
        farm_bar = status_bars.IgnoreBar("farm", _("Huerta"), resp, [], max_points, 0)
        resp_children_bar.append(farm_bar)
        resp.children_list = resp_children_bar
        
        self.second_level = [physica, hygiene, nutrition, fun, resp]
        self.third_level = physica.children_list + hygiene.children_list + nutrition.children_list + fun.children_list + resp.children_list
        
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
