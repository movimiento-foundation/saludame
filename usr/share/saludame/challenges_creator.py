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

from gi.repository import GObject
import challenges
import random

from gettext import gettext as _


def get_mc_challenges():
    
    #First answer is the correct one
    mc_challenges = {}
    
    mc_challenges["physica"] = [
        _create_mc_challenge(u"La actividad física se debe realizar:", [u"Todos los días por lo menos durante 30 minutos.", u"Una vez a la semana.", u"Dos veces en la semana.", u"Cientos de veces en la semana.", u"Una vez al mes.", u"Cinco veces al mes."], 1),
        _create_mc_challenge(u"¿Cuáles de estas acciones sería una actividad física recomendada?", [u"Bailar.", u"Leer.", u"Comer.", u"Mirar TV.", u"Jugar con la XO.", u"Dormir."], 1),
        _create_mc_challenge(u"Cuando vamos a realizar actividad física:", [u"Es importante llevar agua.", u"Debemos realizar actividad física al sol durante los horarios no permitidos.", u"No debemos usar gorro si estamos al sol.", u"No es importante habernos realizado controles médicos previos.", u"No es importante estirar nuestros músculos.", u"No deben hacerlo las personas que padecieron un infarto al corazón."], 1),
        _create_mc_challenge(u"La actividad física:", [u"Nos ayuda a prevenir enfermedades como por ejemplo obesidad, hipertensión arterial y diabetes.", u"No previene la osteoporosis.", u"No nos permite interactuar y conocer otros compañeros.", u"Solo debe ser realizada por personas delgadas.", u"No la pueden realizar obesos.", u"Solo los niños deben realizarla."], 2),
        _create_mc_challenge(u"La actividad física:", [u"Disminuye el estrés.", u"No mejora nuestra digestión.", u"No nos ayuda a descansar mejor y tener un sueño adecuado.", u"No mejora nuestra imagen personal.", u"No nos ayuda a prevenir enfermedades como por ejemplo obesidad, hipertensión arterial diabetes.", u"No previene la osteoporosis."], 2),
        _create_mc_challenge(u"El sedentarismo es:", [u"Un factor de riesgo para enfermedades cardiovasculares.", u"Realizar actividad física todos los días durante al menos 30 minutos.", u"Una enfermedad contagiosa.", u"Una fruta.", u"Una comida.", u"El título de un libro."], 3),
        _create_mc_challenge(u"Acerca de la actividad física:", [u"Todas las veces que hagamos actividad física es muy importante tomar abundante agua para hidratarnos.", u"Antes de realizar actividad física no necesito controlarme con el doctor.", u"Es conveniente para evitar el sedentarismo, pasar más de tres horas diarias sentados frente a la TV, la computadora o el video juegos.", u"Bailar no es una actividad física.", u"La actividad física solo pueden realizarla adultos.", u"Solo tienen que realizar actividad física los escolares."], 3),
        _create_mc_challenge(u"Acerca de la actividad física:", [u"Se dice que una persona es sedentaria cuando su actividad física es inferior a por lo menos media hora diaria y al menos 5 días a la semana.", u"Las personas que tuvieron un infarto no pueden hacer actividad física.", u"Realizar actividad física solo es correr y jugar pelota y no otras actividades como bailar o andar a caballo.", u"Para no ser sedentarios debemos hacer actividad física de moderada intensidad por lo menos 2 días a la semana con una duración de 10 minutos por día.", u"La gran mayoría de las personas no deben realizar actividad física para mantenerse sanos.", u"Solo debo realizar actividad física si tengo sobrepeso."], 4),
        _create_mc_challenge(u"La actividad física:", [u"Mejora nuestra salud cardiovascular.", u"No importa tomar agua cuando realizamos actividad física.", u"Nos hace subir de peso.", u"Solo la deben realizar los adultos.", u"Es menos importante que una buena alimentación.", u"Cuando realizamos actividad física debemos ingerir refrescos cola."], 5),
        _create_mc_challenge(u"¿Cuál se estas afirmaciones acerca de actividad física te parece la correcta?", [u"El 40% de los niños en Uruguay son sedentarios.", u"Es recomendable que estemos jugando en la Xo o mirando tv 5 horas por día.", u"Las personas son sedentarias cuando realizan actividad física 5 veces a la semana.", u"Los niños no necesitan realizar actividad física.", u"No es importante estirar nuestros músculos cuando hacemos actividad física.", u"Cuando realizamos actividad física no debemos ingerir agua."], 5),
        _create_mc_challenge(u"Acerca de la actividad física:", [u"Si realizamos actividad física desde niños podemos prevenir enfermedades cuando seamos más grandes.", u"Las personas que tienen enfermedades cardiovasculares no pueden hacer ningún tipo de actividad física.", u"Los niños pequeños no necesitan hacer actividad física.", u"Los niños que realizan actividad física tienen más probabilidad de enfermarse.", u"Los adultos no tienen que realizar actividad física porque les perjudica su salud.", u"La actividad física solo deben realizarla las personas obesas."], 6),
        _create_mc_challenge(u"La actividad física:", [u"Propicia una buena circulación a todo nuestro organismo.", u"No nos ayuda a controlar nuestro peso corporal.", u"No mejora la actividad de nuestro corazón.", u"No disminuye el estrés y libera tensiones.", u"No mejora nuestra digestión.", u"No mejora nuestra imagen personal."], 7),
        _create_mc_challenge(u"Acerca de nuestras defensas del cuerpo:", [u"Las vacunas nos protegen de enfermedades y trabajan con nuestro sistema inmunológico.", u"Las vacunas no son importantes para cuidar de nuestra salud.", u"Tener las vacunas al día no es importante.", u"El reír, descansar y disfrutar no afecta nuestro sistema inmunológico.", u"Si no nos alimentamos correctamente nuestro sistema inmunológico no se afecta.", u"Las vacunas obligatorias no son gratuitas."], 8),
        _create_mc_challenge(u"Acerca de nuestras defensas del cuerpo:", [u"Una mala alimentación puede afectar nuestras defensas y podemos enfermar.", u"Una buena alimentación no es importante para proteger nuestro sistema inmune.", u"Las vacunas no nos protegen de enfermedades.", u"No es importante revisar mi carné de vacunas.", u"Solo los ancianos deben vacunarse.", u"Si no descansamos nuestro sistema inmune puede verse afectado."], 9),
        _create_mc_challenge(u"Acerca de nuestras defensas:", [u"Reír, descansar y alimentarnos saludablemente aumenta nuestras defensas.", u"Debemos comer pocas frutas y verduras para aumentar nuestras defensas.", u"Descansar y dormir poco aumenta nuestras defensas.", u"Tomar mate únicamente aumenta nuestras defensas.", u"Estar todo el día sin hacer nada aumenta nuestras defensas.", u"El sedentarismo es muy bueno para aumentar nuestras defensas."], 1),
        _create_mc_challenge(u"Acerca de las defensas de nuestro organismo:", [u"Son una barrera que ayudan a que no nos enfermemos.", u"Son un cuadro de fútbol.", u"No son importantes.", u"No ayudan a defendernos de las enfermedades.", u"Es el nombre de un libro de cuentos.", u"Son un grupo de amigos."], 1),
        _create_mc_challenge(u"Acerca del sobrepeso:", [u"Es un factor de riesgo para padecer enfermedades cardiovasculares.", u"Es muy saludable tener sobrepeso.", u"Consumir muchas grasas no nos predispone a tener sobrepeso.", u"Todos los niños deben tener sobrepeso.", u"Si tengo sobrepeso no voy a tener problemas cardiovasculares."], 1),
        _create_mc_challenge(u"Si estoy demasiado delgado:", [u"Pueden afectarse nuestras defensas.", u"Nuestras defensas aumentan.", u"Nuestras fuerzas y energías aumentan.", u"Disminuye el riesgo de enfermar.", u"No es necesario consultar al doctor si estoy demasiado delgado.", u"El control de mi peso en los controles médicos no es importante."], 1),
        _create_mc_challenge(u"Las causas de sobrepeso pueden ser:", [u"Porque no realizo ejercicio.", u"Porque realizo ejercicio.", u"Porque consumo frutas y verduras.", u"Porque consumo muchas naranjas.", u"Porque practico deportes todos los días.", u"Porque consumo una dieta variada."], 1),
        _create_mc_challenge(u"¿En Uruguay cuántos niños tienen sobrepeso?", [u"1 cada cuatro.", u"1 cada un millón.", u"La mitad de los niños del país.", u"3 millones de niños.", u"1 cada cien mil niños.", u"Todos los niños y niñas."], 1),
        _create_mc_challenge(u"El sedentarismo es:", [u"No realizar suficiente actividad física.", u"Jugar con amigos y amigas.", u"Practicar deportes diariamente.", u"Realizar actividades físicas que me gusten.", u"Caminar todos los días.", u"Una infección contagiosa."], 1)                     
    ]
    
    mc_challenges["hygiene"] = [
        _create_mc_challenge(u"Acerca de la salud bucal:", [u"Los dientes deben cepillarse luego de cada comida.", u"Los dientes deben cepillarse sin pasta dental.", u"Lo dientes no deben cepillarse.", u"Los dientes deben cepillarse solo después de comer carne.", u"Solo se deben cepillar los dientes si comí chicle.", u"Es muy recomendable comer golosinas y no cepillarse los dientes."], 1),
        _create_mc_challenge(u"Los niños y adolescentes deben cepillar sus dientes:", [u"Cada vez que consumen un alimento.", u"Dos veces al día.", u"Tres veces al día.", u"Cinco veces al día.", u"Cuando vamos a realizar ejercicio.", u"Cuando vamos a nadar."], 1),
        _create_mc_challenge(u"Para mantener una correcta higiene y estar saludable debo:", [u"Bañarme con agua y jabón todos los días.", u"Lavarme las manos después de comer.", u"Lavarme las manos únicamente para comer.", u"Bañarme con agua y jabón una vez a la semana.", u"Lavarme las manos sin agua y jabón.", u"Cepillar mis dientes una vez al día."], 1),
        _create_mc_challenge(u"En relación a los hábitos higiénicos: ", [u"Antes de manipular los alimentos, prepararlos y consumirlos, debemos lavarnos las manos por lo menos durante 30 segundos.", u"No es importante ducharnos todos los días.", u"Cuando nos duchamos es importante que sea sin jabón.", u"Estando limpios no prevenimos enfermedades.", u"Los niños deben bañarse solo una vez a la semana.", u"Los niños deben bañarse día por medio."], 1),
        _create_mc_challenge(u"En relación al lavado de manos, indique cuál es la oración correcta:", [u"El primer paso es mojarnos las manos con agua.", u"El primer paso es pasarnos jabón.", u"El alcohol en gel es mucho mejor que lavado con agua y jabón.", u"El lavado de manos no es una buena medida para prevenir enfermedades.", u"Solo en la escuela debo lavar mis manos.", u"Solo cuando voy al baño debo lavar mis manos."], 1),
        _create_mc_challenge(u"Acerca del lavado de manos, ¿qué opción es verdadera?", [u"El primer paso que debemos realizar es mojarnos las manos con agua.", u"El primer paso que debemos realizar es lavarnos las manos con agua sucia o estancada.", u"El primer paso que debemos realizar es colocar jabón en nuestras manos.", u"Si lavo mis manos no es importante lavar mis uñas.", u"Después de estornudar y sonar mi nariz no es necesario lavar mis manos.", u"El lavado de manos después de tocar un animal no es importante."], 1),
        _create_mc_challenge(u"Es recomendable visitar al dentista:", [u"Una vez cada 6 meses.", u"Una vez cada 10 años.", u"Una vez cada 1 mes.", u"Una vez cada 2 días.", u"Una vez cada 5 años.", u"Una vez por semana."], 1),
        _create_mc_challenge(u"En relación al lavado de manos:", [u"Es muy importante enseñar a otros niños y a nuestras familias a lavarnos correctamente las manos.", u"Lavarnos las manos es menos importante que alimentarnos bien.", u"Debemos lavarnos las manos solo cuando sonamos nuestras narices.", u"El lavado de manos debe ser antes de sonar nuestras narices.", u"Las manos se lavan solo cuando las vemos sucias.", u"Las manos se lavan solo cuando vamos a comer."], 2),
        _create_mc_challenge(u"Acerca de la salud bucal:", [u"Es recomendable visitar el dentista y ver cómo están mis dientes para prevenir enfermedades y aprender a cuidar mi salud bucal.", u"Los dientes solo se cepillan si están sucios.", u"Los dientes de leche no se cepillan.", u"Solo los niños grandes deben cepillar los dientes.", u"Los bebés no tienen que visitar al dentista.", u"Solo los adultos deben ir al dentista."], 2),
        _create_mc_challenge(u"Acerca de la salud bucal, marque la opción verdadera.", [u"El cepillado debe realizarse desde las encías hacia los dientes.", u"El cepillado debe realizarse desde los dientes hacia las encías.", u"El cepillado puede realizarse con los dedos.", u"Los alimentos ricos en azúcares no influyen en nuestra salud bucal.", u"Solo los dientes permanentes se cepillan, los de leche no es necesario que los cepille.", u"Si perdemos un diente con un traumatismo o golpe debemos tirarlo a la basura."], 3),
        _create_mc_challenge(u"Acerca de la salud bucal: ", [u"En la escuela se puede enseñar a los demás compañeros la técnica del cepillado de dientes para después entre todos enseñar en nuestra casa a los demás.", u"Tener mal aliento es agradable.", u"Tener dientes sanos y blancos no es agradable.", u"Los dientes no deben cepillarse siempre luego de cada comida.", u"No es importante enseñarle a los más pequeños en la escuela, cómo se cepillan los dientes.", u"No es importante enseñar a nuestra familia y amigos, cómo cuidar de nuestra salud bucal."], 3),
        _create_mc_challenge(u"Para evitar que se enfermen mis dientes es recomendable:", [u"Realizar controles con el odontólogo.", u"Comer muchas golosinas.", u"Fumar.", u"Cepillar mis dientes solo cuando ingiero dulces.", u"Cepillar mis dientes 10 veces al día.", u"Cepillar mis dientes una vez al día."], 4),
        _create_mc_challenge(u"Acerca de la salud bucal: ", [u"El mal aliento puede estar significando que mis dientes o encías están enfermos.", u"Solo deben cepillarse los dientes pero no las encías.", u"Solo deben cepillarse los dientes pero no la lengua.", u"Si no me duelen los dientes o las muelas no debo ir al dentista.", u"Los dientes no deben cepillarse.", u"Los dientes de leche no se deben cepillar."], 4),
        _create_mc_challenge(u"En relación a la seguridad de los alimentos:", [u"La carne debe almacenarse en la heladera.", u"Cuando guardamos harinas, azúcares u otros alimentos debemos hacerlo en recipientes abiertos.", u"La carne debe dejarse al aire libre.", u"Los alimentos deben guardarse junto a productos químicos o venenos.", u"Los alimentos crudos se guardan junto a los cocidos en el mismo recipiente.", u"Los huevos no deben almacenarse en la heladera."], 5),
        _create_mc_challenge(u"¿Qué conoces acerca de la salud bucal?", [u"Los alimentos ricos en calcio y flúor son muy importantes para mis dientes.", u"Debo consumir muchos alimentos ricos en azúcares para cuidar mis dientes.", u"Los bebés no necesitan visitar al odontólogo.", u"Una alimentación variada rica en frutas y verduras no es importante para el cuidado de mis dientes.", u"Los dientes de leche no necesitan cepillarse.", u"Solo debo visitar al dentista cuando me duele algún diente."], 5),
        _create_mc_challenge(u"Es recomendable que los controles con el dentista u odontólogo se realicen cada:", [u"6 meses", u"2 años", u"1 mes", u"15 días", u"6 años", u"10 años"], 6),
        _create_mc_challenge(u"En relación a la seguridad de los alimentos:", [u"Los alimentos, como carnes y derivados, deben colocarse en heladera lo más rápidamente posible luego de comprados.", u"Lavar las frutas y verduras solo si voy a consumirlas con cáscara.", u"No es necesario lavar frutas y verduras con agua e hipoclorito de sodio (cloro).", u"Es recomendable re-congelar o volver a congelar un alimento que ya fue descongelado.", u"Si los vamos a descongelar podemos hacerlo directamente colocándolos a temperatura ambiente.", u"Si tenemos mascotas no es importante mantenerlas lejos de nuestros alimentos."], 6),
        _create_mc_challenge(u"En relación a la seguridad de los alimentos:", [u"No deberíamos consumir huevos poco cocidos, mayonesas caseras, o merengues crudos, por el peligro de padecer una enfermedad que se llama salmonelosis.", u"Cuando manipulamos carnes o huevos no es importante lavar con agua caliente y jabón todos los utensilios de cocina que utilizamos.", u"Cuando guardamos harinas, fideos secos y/o azúcar, debemos hacerlo en lugares abiertos al contacto de insectos y roedores.", u"La carne, fiambres, huevos, leche y/o manteca, deben ser almacenados a temperatura ambiente.", u"Manipular los alimentos en forma higiénica no es muy importante para evitar la contaminación por microbios."], 7),
        _create_mc_challenge(u"¿Cuál de estas afirmaciones es la verdadera?", [u"El hábito de fumar afecta y perjudica seriamente nuestra salud bucal.", u"El hábito de fumar no afecta nuestra salud bucal.", u"No es necesario cepillar los dientes de “leche”.", u"Es necesario cepillarse los dientes solo cuando consumimos dulces.", u"Los dientes deben cepillarse sin pasta de dientes.", u"Mantener nuestros dientes sanos y fuertes no es importante."], 8),
        _create_mc_challenge(u"¿Cuál de estas opciones te parece verdadera?", [u"La cáscara de las frutas son ricas en vitaminas.", u"Las verduras deben lavarse con agua estancada y sin hipoclorito.", u"Las verduras no deben lavarse si las vamos a cocinar.", u"Se deben consumir todos los días frutas pero no verduras.", u"La cáscara de la fruta no es rica en vitaminas.", u"No es recomendable consumir frutas porque dañan nuestra salud."], 9)                            
    ]
    
    mc_challenges["nutrition"] = [
        _create_mc_challenge(u"¿Cuántas porciones de frutas y verduras deben consumirse diariamente?", [u"5", u"1", u"2", u"3", u"0", u"Media"], 1),
        _create_mc_challenge(u"¿Cuántas porciones de carnes debo consumir diariamente?", [u"2 a 3 porciones diarias", u"5 porciones diarias", u"1 porción diaria", u"7 porciones diarias", u"10 porciones diarias", u"4 porciones diarias"], 1),
        _create_mc_challenge(u"¿Cuántas porciones de cereales y leguminosas se recomienda consumir diariamente?", [u"5 a 7 porciones diarias.", u"10 porciones diarias.", u"7 galletas de campaña por día.", u"1 porción diaria.", u"2 porciones diarias.", u"8 porciones diarias."], 1),
        _create_mc_challenge(u"¿Cuántas porciones de lácteos, yogures o quesos se recomienda consumir diariamente?", [u"2 porciones diarias.", u"1 porción diaria.", u"5 porciones diarias.", u"10 porciones diarias.", u"Un litro de leche por día.", u"2 litros de yogurt por día."], 1),
        _create_mc_challenge(u"¿Cuántas porciones de grasas y aceites deben consumirse diariamente?", [u"Entre 2 y 3.", u"10", u"11", u"7", u"8", u"5"], 1),
        _create_mc_challenge(u"¿Cuántas porciones de azúcares y dulces se recomienda consumir diariamente?", [u"4 y 5 porciones diarias.", u"1 porción diaria.", u"2 porciones diarias.", u"3 porciones diarias.", u"7 porciones diarias.", u"Media porción diaria."], 1),
        _create_mc_challenge(u"Es muy saludable:", [u"Comer frutas y verduras todos los días.", u"Consumir grandes cantidades de grasas saturadas.", u"Consumir asado con mucha grasa.", u"Consumir mucha sal en los alimentos.", u"Consumir poca fruta y verdura.", u"No consumir leche o alimentos lácteos."], 1),
        _create_mc_challenge(u"¿Qué alimentos contienen alto contenido de grasas?", [u"Algunos cortes de carnes.", u"Los cereales.", u"La manzana.", u"La frutilla.", u"Los quesos magros.", u"El pan integral."], 1),
        _create_mc_challenge(u"¿Cuál es la principal función de los hidratos de carbono?", [u"Nos aportan energía.", u"Nos permiten tener uñas y cabello fuertes.", u"Nos oxigenan.", u"Nos otorgan anticuerpos.", u"Nos permiten absorber calcio."], 1),
        _create_mc_challenge(u"¿Qué alimento es parte del grupo frutas y verduras?:", [u"Las naranjas.", u"Los alfajores.", u"El asado.", u"Las golosinas.", u"El helado.", u"El pan."], 1),
        _create_mc_challenge(u"Las grasas saturadas:", [u"Se encuentran en varios cortes de carne de vaca.", u"Se encuentran en las frutas.", u"No favorecen el desarrollo de ateroesclerosis.", u"Son muy buenas para la salud.", u"Aumentan los niveles de HDL o colesterol bueno.", u"Son el alimento ideal."], 2),
        _create_mc_challenge(u"Consumir pocas grasas saturadas es importante porque:", [u"Puede provocarnos ateroesclerosis.", u"Nos provoca diarrea.", u"Nos provoca dolor de cabeza.", u"Nos provoca sed.", u"Nos provoca sueño."], 2),
        _create_mc_challenge(u"El agua: ", [u"Regula nuestra temperatura corporal.", u"No permite el transporte de nutrientes a las células.", u"Los alimentos no contienen agua.", u"Las necesidades de agua varían entre 10 y 20 litros por día en las personas.", u"Cuando tenemos diarrea no es importante tomar agua.", u"No es necesario lavar los alimentos con agua."], 2),
        _create_mc_challenge(u"Acerca del consumo de sal: ", [u"Los alimentos naturalmente ya contienen sal, por eso se recomienda no abusar del agregado de sal o incluso no utilizar sal en los alimentos.", u"Solo los niños deben controlar su presión arterial.", u"Los adultos son los únicos que deben controlar su presión arterial.", u"Solo las personas hipertensas deben controlar su presión arterial.", u"Lo recomendable es consumir los alimentos con abundante cantidad de sal.", u"La toma de presión arterial en mis controles de salud no es importarte."], 2),
        _create_mc_challenge(u"Las grasas saturadas:", [u"Debemos consumirlas con precaución.", u"Mejoran nuestra salud cardiovascular.", u"Hay que consumirlas en exceso.", u"Las encontramos en la zanahoria.", u"Las encontramos en las frutas y verduras.", u"Se encuentran en la manzana."], 3),
        _create_mc_challenge(u"¿Qué conoces acerca de las grasas? Elije la opción verdadera.", [u"El colesterol LDL o “malo“ es el colesterol que se acumula en las arterias y nos puede traer muchos problemas cardiovasculares.", u"Si consumimos muchos alimentos ricos en colesterol nos volvemos más saludables.", u"El colesterol debe consumirse en exceso a diferencia de las frutas que se deben consumir en muy pocas cantidades.", u"Debemos tener una alimentación rica en grasas saturadas.", u"Las grasas saturadas se encuentran en la lechuga.", u"Las grasas saturadas se encuentran en el tomate."], 3),
        _create_mc_challenge(u"Las grasas saturadas: ", [u"Deben consumirse pero con moderación.", u"Hay que consumirlas de forma libre sin importar la cantidad.", u"Son muy saludables.", u"Son tan buenas como el ejercicio físico.", u"Son el alimento más nutritivo para nuestra salud.", u"Se encuentran en los duraznos."], 3),
        _create_mc_challenge(u"¿Cuál de estas opciones es la verdadera?", [u"La mayoría de los alimentos contienen naturalmente la cantidad de sal necesaria.", u"Es recomendable consumir alimentos fritos en vez de hervidos o al horno.", u"Es recomendable agregarle sal a los alimentos.", u"Al agregarle sal a los alimentos evitamos desarrollar hipertensión arterial.", u"Las verduras contienen muchas grasas saturadas.", u"Los fiambres y embutidos deben consumirse diariamente."], 3),
        _create_mc_challenge(u"¿Conoces los grupos de alimentos? Encuentra la opción correcta.", [u"El grupo de frutas y verduras incluye acelga, cebolla, espinaca, banana, manzana, tomate, zapallito, rabanito, morrón y muchas más.", u"El grupo de azúcares y dulces incluye grasa vacuna, grasa de cerdo, manteca, margarina, aceites vegetales (arroz, girasol, oliva, maíz, soya) y frutas secas.", u"El grupo de las grasas incluye azúcar, miel, dulces, mermeladas y frutas, dulce de leche y golosinas.", u"El grupo de las frutas y verduras incluye trigo, maíz, arroz, cebada, avena y centeno.", u"El grupo de las carnes incluye los dulces, mermeladas y frutas, dulce de leche y golosinas.", u"El grupo de las leches y derivados incluye harina de trigo, sémola, féculas, polenta, tapioca, gofio, panes, bizcochos, galletas, galletitas y pastas de todo tipo."], 4),
        _create_mc_challenge(u"¿Qué sabes en relación a las fibras en los alimentos?", [u"La fibra alimentaria nos ayuda a movilizar el intestino sin dificultad.", u"La fibra alimentaria no regula funciones intestinales.", u"Si realizamos actividad física no movilizamos nuestro intestino sin dificultad.", u"El consumo de frutas no ayuda a movilizar nuestro intestino sin dificultad.", u"La fibra alimentaria no ayuda a regular el colesterol en nuestro organismo.", u"El consumo de agua y de frutas y verduras no ayuda a que movilicemos el intestino sin dificultad."], 4),
        _create_mc_challenge(u"Las grasas saturadas:", [u"Se encuentran en la carne de cerdo.", u"Se encuentran en la naranja.", u"Se encuentran en las verduras.", u"Aumentan el colesterol bueno o HDL.", u"Son muy buenas para nuestra salud cardiovascular.", u"Debemos consumirlas todos los días en grandes cantidades."], 4),
        _create_mc_challenge(u"Debemos aumentar nuestra ingesta de agua cuando:", [u"Tenemos diarrea.", u"Nos reímos.", u"Leemos.", u"Jugamos con la computadora.", u"Jugamos a las cartas.", u"Escuchamos música."], 5),
        _create_mc_challenge(u"Los micronutrientes son:", [u"Las vitaminas y los minerales.", u"Los glúcidos o carbohidratos.", u"Los lípidos o grasas.", u"Las proteínas.", u"El asado.", u"El salame."], 5),
        _create_mc_challenge(u"Acerca de los minerales:", [u"Si no consumimos alimentos ricos en hierro podremos padecer anemia.", u"La sal es fundamental y debemos agregarla en todos los alimentos.", u"Los alimentos no contienen sal en su forma natural.", u"Las lentejas, los huevos y la carne no son alimentos ricos en hierro.", u"El bajo consumo de calcio en la dieta no nos provoca osteoporosis a largo plazo.", u"Nuestro organismo produce constantemente minerales por eso no es necesario consumirlos."], 5),
        _create_mc_challenge(u"¿Qué consejo es el verdadero?", [u"Para mantener la salud, es importante realizar diariamente una alimentación variada que incluya alimentos de los seis grupos.", u"No es importante consumir diariamente verduras y frutas de estación.", u"No es importante controlar su consumo de carnes, fiambres, embutidos, manteca, margarina, mayonesa y frituras por su alto contenido en grasas.", u"No es importante disminuir el consumo de sal.", u"Para rendir más durante el día no es necesario comenzar con un desayuno que incluya leche, pan y fruta."], 6),
        _create_mc_challenge(u"Las proteínas son macronutrientes y las podemos encontrar en:", [u"Carnes y huevos ", u"Las golosinas", u"Refrescos", u"Manteca", u"Dulces", u"Chocolate"], 6),
        _create_mc_challenge(u"¿Cuál de éstos es un macronutriente? ", [u"Las proteínas.", u"Vitaminas.", u"Minerales.", u"La sal.", u"El flúor.", u"El calcio."], 6),
        _create_mc_challenge(u"¿Acerca de las vitaminas, cuál es la opción verdadera?", [u"Son vitales para el organismo.", u"Las vitaminas son todas fabricadas por nuestro propio organismo.", u"Las vitaminas no son importantes.", u"La falta de vitaminas no nos produce enfermedades.", u"La cáscara de las frutas no contiene vitaminas.", u"Cocinar las frutas y verduras con una olla al vapor no nos conserva las vitaminas"], 7),
        _create_mc_challenge(u"¿Cuál de estos consejos de las guías GABA es el correcto?", [u"La alimentación debe ser variada e incluir alimentos de los 6 grupos.", u"Para rendir más durante el día debemos incluir un desayuno que contenga asado.", u"Comer sin importar las porciones indicadas en los grupos de alimentos.", u"Los lácteos no son necesarios en todas las edades.", u"Consumir una vez a la semana frutas de estación.", u"Aumentar el consumo de bebidas azucaradas."], 7),
        _create_mc_challenge(u"En relación a las vitaminas que se encuentran en frutas y verduras: ", [u"Se conservan mejor si consumo frutas y verduras con cáscara porque muchas vitaminas se concentran en la cáscara.", u"Se conservan mejor en las frutas y verduras si las hiervo durante un tiempo prolongado.", u"Se conservan mejor si las consumo fritas.", u"Las vitaminas no se encuentran en las frutas.", u"La vitamina A se encuentra en el tomate.", u"La vitamina A se encuentra en el limón."], 7),
        _create_mc_challenge(u"Las fibras en la alimentación:", [u"Ayudan a regularizar nuestro tránsito intestinal junto al agua y el ejercicio.", u"No ayudan a movilizar nuestro intestino.", u"No son tan importantes.", u"Se encuentran en el asado.", u"Se encuentran en las golosinas.", u"No se encuentran en las frutas."], 8),
        _create_mc_challenge(u"¿Cuál de estos consejos es el verdadero?", [u"Es importante incluir frutas en el desayuno.", u"No es necesario separar alimentos crudos de los cocidos.", u"No es importante lavar los alimentos con agua y jabón.", u"No es necesario guardar la carne en la heladera.", u"Los niños deben consumir media fruta por día.", u"No es importante limpiar el lugar donde voy a cocinar."], 8),
        _create_mc_challenge(u"¿Cuál de estos consejos de las guías GABA es el correcto?", [u"Controlar el consumo de carnes, fiambres y embutidos.", u"Aumentar el consumo de sal.", u"Elegir los alimentos más caros.", u"No es importante cuidar la higiene de los alimentos.", u"Consumir muchas grasas saturadas.", u"Consumir mucha mayonesa."], 8),
        _create_mc_challenge(u"Acerca de los lácteos y derivados:", [u"El consumo de alimentos ricos en calcio, como la leche y los quesos, es muy importante para prevenir la osteoporosis.", u"La leche y los quesos son productos pobres en calcio.", u"El consumo de alimentos ricos en calcio no es importante.", u"Es necesario consumir alimentos ricos en calcio solo cuando somos niños.", u"Solo los adultos deben consumir alimentos ricos en calcio.", u"Solo los bebés deben consumir leche."], 9),
        _create_mc_challenge(u"Acerca de la seguridad de los alimentos:", [u"La leche que consumimos debe ser pasteurizada y en caso de no serlo, debemos hervirla para evitar gérmenes que pueden ser muy perjudiciales.", u"Los huevos se pueden consumir poco cocidos o crudos porque son seguros.", u"Deberíamos consumir huevos poco cocidos y mayonesa casera.", u"La carne debe conservase fuera de la heladera.", u"Los alimentos crudos deben guardarse en el mismo recipiente que los cocidos.", u"Si tenemos animales no es necesario desparasitarlos si están lejos de la comida que vamos a consumir."], 9)                                                                               
    ]
    
    mc_challenges["spare_time"] = [
        _create_mc_challenge(u"Es muy saludable:", [u"Tomar entre 2 y 3 litros de agua por día.", u"Trabajar y estudiar sin parar todo el día todos los días.", u"No controlarnos con el doctor para saber cómo estamos.", u"Exponernos al sol sin gorro.", u"Comer muchos asados con mucha grasa.", u"No desayunar."], 1),
        _create_mc_challenge(u"Es muy saludable:", [u"Bañarnos con agua y jabón todos los días.", u"Lavar nuestras manos una vez al día.", u"Cepillar nuestros dientes una vez al día.", u"Realizarnos controles médicos una vez cada 10 años.", u"Cepillar nuestros dientes solo cuando comemos dulces.", u"Realizar actividad física una vez al mes."], 1),
        _create_mc_challenge(u"¿Cuántos horas de sueño promedio necesita un joven cada noche?", [u"8 horas", u"5 horas", u"6 horas", u"10 horas", u"11 horas", u"4 horas"], 1),
        _create_mc_challenge(u"¿Por qué es importante descansar y dormir?", [u"Para recuperar energía.", u"Porque no tenemos nada que hacer.", u"No se ve nada en la noche.", u"Porque durmiendo aprendemos la información de la escuela.", u"Para evitar la diarrea.", u"Para que nuestros músculos sean más fuertes."], 1),
        _create_mc_challenge(u"Es importante practicar deporte:", [u"Para ejercitar el cuerpo, la digestión y evitar enfermedades cardiovasculares.", u"Para ganar, evitar enfermedades cardiovasculares y hacerse ver.", u"Para hacerse ver, dar la XO tiempo para cargar y ser musculoso.", u"Para evitar estreñimiento, inflar nuestros pulmones y eludir tareas domésticas.", u"Para evitar dolor de panza, dormir mejor y ser más feliz.", u"Para quemar grasas corporales, dar a mi caballo tranquilidad y ser el mejor."], 1),
        _create_mc_challenge(u"En mi tiempo libre es importante jugar:", [u"Para desarrollar mi imaginación y porque es un derecho humano.", u"Porque es un derecho humano y para eludir tareas domésticas.", u"Porque es importante para dormir mejor y comer más.", u"Para que el día pase rápido y aprender sobre la vida.", u"Para olvidar la escuela y estar solo.", u"Para disfrutar con amigos y ser tramposo."], 1),
        _create_mc_challenge(u"Lo más importante de jugar deportes con amigos es:", [u"Jugar juntos.", u"Prevenir lesiones.", u"Ganar.", u"Ser muscoloso.", u"Que los otros ganen.", u"Ser popular."], 1),
        _create_mc_challenge(u"En mi tiempo de ocio se puede:", [u"Divertirse y desarrollarse personalmente.", u"Dormir mucho y comer todo el día.", u"Ver televisión y negar el ambiente social.", u"Aburrirse y quejarse.", u"Evitar las tareas escolares y domésticas.", u"Estar todo el día en la calle y hacer travesuras."], 1),
        _create_mc_challenge(u"Está bien practicar deportes para evitar:", [u"Enfermedades cardiovasculares.", u"Las tareas de la escuela.", u"Mi familia.", u"Las tareas del campo.", u"Mis amigos.", u"Mis problemas."], 1),
        _create_mc_challenge(u"¿Qué actividad consume más energía corporal?", [u"Jugar fútbol.", u"Escribir una carta.", u"Jugar en la XO.", u"Pelar una manzana.", u"Escribir en el pizarrón.", u"Hacer un dibujo."], 1),
        _create_mc_challenge(u"Durante el recreo lo más importante es:", [u"Disfrutar y jugar.", u"Pelear y jugar.", u"Quejarse y comer.", u"Hacer travesuras y molestar.", u"No hacer nada y beber refresco.", u"Jugar en la XO y gritar fuerte."], 1),
        _create_mc_challenge(u"Es importante tener tiempo libre con mi familia:", [u"Para divertirse y hacer cosas juntos.", u"Para limpiar y hablar.", u"Para hablar y trabajar en el campo.", u"Para hacer nada y ver televisión.", u"Para divertirse y limpiar.", u"Para hacer asado y comer mucho."], 1),
        _create_mc_challenge(u"Soy responsable en el uso de mi tiempo libre al:", [u"Elegir las actividades que más me gustan.", u"Ganar trofeos.", u"Ser muy conocido.", u"No cuidar mi salud.", u"Evitar socializar con los otros.", u"Aburrirse mucho."], 1),
        _create_mc_challenge(u"En el tiempo libre se disfruta leer para:", [u"Aprender y conocer más del mundo.", u"Evitar amigos y familia.", u"Crecer el conocimiento y comer mucho mientras se lee.", u"Evitar problemas escolares y personales.", u"Tener distracción y pasar el tiempo.", u"Estar adentro y no hacer tareas en el campo."], 1),
        _create_mc_challenge(u"Durante el juego está prohibido:", [u"Obligar a otros a hacer lo que yo diga.", u"Ganar.", u"Escuchar al árbrito.", u"Aceptar las reglas.", u"Tomar agua.", u"Disfrutar."], 1),
        _create_mc_challenge(u"Durante el juego se tiene que respetar:", [u"Las reglas y a los otros.", u"El egoísmo y el tiempo del juego.", u"Solo tus deseos y no el de los demás.", u"El tiempo del juego y no aceptar las variantes.", u"El ambiente donde se juega y dejar todo sucio.", u"Quebrar las reglas y hacer lo que quieren los demás."], 1),
        _create_mc_challenge(u"El ocio es:", [u"Una forma positiva de aprovechar el tiempo libre.", u"Una receta de cocina.", u"Una forma negativa para pasar el día.", u"Una forma de construir una casa.", u"Un derecho para mi mascota.", u"Una forma física."], 1),
        _create_mc_challenge(u"El ocio no es:", [u"Una manera de perder el tiempo.", u"Una manera de divertirse.", u"Un tiempo para crear.", u"Un tiempo para jugar.", u"Un tiempo para disfrutar con otros.", u"Un tiempo para estar con la familia."], 1),
        _create_mc_challenge(u"No es deporte:", [u"Trabajar en la huerta.", u"Saltar la cuerda.", u"Jugar al fútbol.", u"Correr.", u"Bailar.", u"Domar caballos."], 1),
    ]
    
    mc_challenges["responsability"] = [
        _create_mc_challenge(u"Lo primero que debemos determinar para realizar nuestra huerta es:", [u"El terreno.", u"Qué vamos a sembrar.", u"Cómo lo vamos a cercar.", u"Quién lo va a trabajar.", u"Cómo va a ser el riego.", u"Cómo protegerla del sol."], 1),
        _create_mc_challenge(u"¿Cuál es la parte más importante, trabajando en la huerta?", [u"Todas.", u"La siembra.", u"La elección de semillas.", u"La cosecha.", u"Separar las semillas.", u"El riego."], 1),
        _create_mc_challenge(u"Los controles de salud con el doctor sirven para:", [u"Aprender a cuidar de mi salud y prevenir enfermedades.", u"Aprender matemáticas.", u"Aburrirme.", u"Aprender las tablas.", u"Perder el tiempo.", u"Aprender a leer."], 1),
        _create_mc_challenge(u"En relación a los controles de salud, ¿cuál es la opción correcta?", [u"Todas las personas tienen derecho a poder controlar su salud.", u"Solo deben controlarse los bebés.", u"Solo deben controlarse los niños.", u"Solo deben controlarse los adultos.", u"Solo deben controlarse los ancianos.", u"Solo deben controlarse los escolares."], 1),
        _create_mc_challenge(u"En relación a los controles de salud, ¿cuál es la opción correcta?", [u"Los niños tienen derecho a que los adultos los lleven a controlar su salud.", u"La frecuencia de controles de salud es igual para todas las edades.", u"En los controles de salud no aprendemos a cuidarnos y a alimentarnos correctamente.", u"Los controles de salud no son importantes.", u"Los controles de salud no me permiten aprender cosas acerca de mi salud."], 1),
        _create_mc_challenge(u"¿Cuándo debo concurrir al doctor?", [u"Debo concurrir al menos una vez por año a controlar mi salud.", u"Únicamente cuando estoy enfermo.", u"Una vez cada 5 años.", u"Una vez cada 2 años.", u"Solo cuando me siento enfermo.", u"Solo cuando me duele la cabeza."], 1),
        _create_mc_challenge(u"Cuando voy a mis controles de salud es importante que el doctor revise:", [u"Mi peso.", u"Mi Xo.", u"Mis notas en la escuela.", u"Mi mascota.", u"Mi ropa.", u"Mis zapatos."], 1),
        _create_mc_challenge(u"¿Qué cuidados debo tener si vamos a nadar?", [u"Debemos siempre concurrir con un adulto.", u"Podemos ir solos y no importa que un adulto nos acompañe.", u"Debemos nadar contra la corriente.", u"Si no sé nadar es recomendable bañarme en lo hondo.", u"Si llevamos algo inflable para jugar no es necesario atarlo.", u"No hay que aprender cuidados para ir a nadar porque no es peligroso."], 1),
        _create_mc_challenge(u"Acerca de las vacunas:", [u"Las vacunas son una importante barrera inmunológica que nos protegen de enfermedades.", u"No tiene importancia vacunarnos cuando ya somos niños grandes.", u"Tener un carné de vacunas no es importante.", u"El doctor en mis controles de salud no necesita saber si estoy correctamente vacunado.", u"Solo los niños pequeños deben tener su carné de vacunas al día.", u"Si estoy sano no necesito vacunarme."], 1),
        _create_mc_challenge(u"Si vamos a exponernos al sol, elije la opción verdadera.", [u"Es recomendable que busquemos lugares de sombra.", u"Es recomendable que vayamos de ropa oscura.", u"Es recomendable que llevemos poca agua.", u"No es necesario usar protector solar.", u"No es necesario usar lentes de sol.", u"La mejor hora para exponernos al sol es a la una de la tarde."], 1),
        _create_mc_challenge(u"Acerca del agua:", [u"Si no sé nadar es recomendable que no entre al agua.", u"No es recomendable que vayamos al agua solos.", u"Si sé nadar no es importante que me acompañe un adulto al agua.", u"El fondo de los ríos, arroyos y lagos siempre es el mismo y no cambia nunca.", u"No es necesario atar los inflables que llevamos al agua.", u"Cuando vamos a nadar el agua debe llegar hasta nuestro cuello."], 1),
        _create_mc_challenge(u"Uno de los materiales fundamentales para la construcción de la huerta es:", [u"Pala ancha.", u"Escavadora.", u"Nylon.", u"Tractor.", u"Alambre.", u"Clavos."], 1),
        _create_mc_challenge(u"Es conveniente que la huerta sea de forma:", [u"Rectangular.", u"Circular.", u"Triangular.", u"Hexagonal.", u"Piramidal.", u"Romboidal."], 2),
        _create_mc_challenge(u"¿Cuál de estos animales es enemigo de nuestras plantas en la huerta?", [u"El pulgón.", u"El San Antonio Rojo.", u"La rana.", u"El sapo.", u"Las arañas.", u"Los murciélagos."], 2),
        _create_mc_challenge(u"En mis controles de salud:", [u"Debo controlar cómo veo y están mis ojos.", u"Debo controlar mis deberes.", u"Debo controlar mi carné escolar.", u"No es importante saber cómo está mi altura.", u"No es importante saber cuánto peso.", u"No es importante pedir que me lleven a mis controles de salud."], 2),
        _create_mc_challenge(u"¿Cuál de estas opciones es la verdadera?", [u"Todas las personas deben tener su carné de vacunas al día.", u"Las vacunas no influyen en nuestras defensas.", u"Recibir vacunas no es importante porque la buena alimentación ya nos aporta defensas.", u"Solo los adultos deben vacunarse.", u"Las vacunas no son importantes.", u"Solo los niños pequeños deben vacunarse."], 2),
        _create_mc_challenge(u"Si vamos a exponernos al sol, elije la opción verdadera.", [u"El gorro recomendable para estar al sol debería ser de ala ancha, que proteja orejas, cara y cuello.", u"Los rayos UV solo dañan nuestra piel y no otras partes de nuestro organismo.", u"Si vamos a exponernos al sol debemos usar gorro sin visera.", u"Es recomendable que la ropa que usemos sea blanca.", u"No es importante consultar al doctor si me encuentro un lunar sospechoso en mi piel.", u"El examen de mi piel no es importante cuando voy a mis controles médicos."], 3),
        _create_mc_challenge(u"Para estar seguros cuando vamos al agua debemos hacer pie y además:", [u"El agua debe llegarnos hasta la cintura.", u"El agua debe llegarnos hasta los labios.", u"El agua debe llegarnos hasta los tobillos.", u"El agua debe llegarnos hasta las rodillas.", u"El agua debe llegarnos hasta el cuello.", u"El agua debe llegarnos hasta la nariz."], 3),
        _create_mc_challenge(u"Uno de los métodos de siembra en nuestra huerta es:", [u"El directo.", u"En línea.", u"Al voleo.", u"En casilla.", u"En un hueco.", u"Hidroponia."], 3),
        _create_mc_challenge(u"Sobre la huerta: es más fácil cuidar de las semillas sembrando:", [u"En almácigos.", u"Directamente en la tierra.", u"Al voleo.", u"En línea.", u"En casillas o hueco.", u"En agua."], 3),
        _create_mc_challenge(u"Los canteros de la huerta deben estar:", [u"Un poco por arriba del nivel del suelo.", u"15 cm. por debajo del nivel del suelo.", u"1 metro arriba del nivel del suelo.", u"A ras del suelo.", u"a 1 metro de profundidad.", u"a 50 cm. de profundidad."], 4),
        _create_mc_challenge(u"Acerca de mis derechos y obligaciones en relación a mi salud, la opción verdadera es:", [u"En la escuela puedo ayudar a los más pequeños a aprender a cepillar sus dientes.", u"No es importante ser responsable a la hora de exponernos al sol.", u"Cuando vamos a nadar debemos ir solos sin un adulto que nos acompañe.", u"No es importante enseñar a mi familia y mis compañeros hábitos saludables acerca de nuestra salud.", u"Estar vacunados con las vacunas obligatorias no es importante.", u"Los únicos que deben vacunarse son los niños pequeños."], 4),
        _create_mc_challenge(u"¿Cuáles son los horarios recomendados para exponernos al sol en verano?", [u"Antes de las 11:00 o después de las 17:00.", u"A las 12:00 horas.", u"A las 16:00 horas.", u"A las 13:00 horas.", u"A las 15:00 horas", u"A las 14:00 horas."], 4),
        _create_mc_challenge(u"La orientación de las camas altas o canteros de nuestra huerta debe ser:", [u"Norte-Sur.", u"Este-Oeste.", u"Sur-Este.", u"Norte-Oeste.", u"Sur-Oeste.", u"Este-Norte."], 4),
        _create_mc_challenge(u"Ante la presencia de plagas en nuestra huerta debemos usar:", [u"Productos no tóxicos.", u"Agroquímicos.", u"Fuego.", u"Hipoclorito de sodio.", u"Detergente.", u"Alcohol."], 5),
        _create_mc_challenge(u"¿Cuál de estos pasos no es parte de la construcción de una huerta?", [u"Colocar las semillas.", u"Clavar las estacas en cada una de las esquinas del lugar elegido.", u"Limpiar la superficie, sacando piedras, vidrios y basura.", u"Marcar las camas altas.", u"Sacar la tierra de las camas altas con una profundidad de 15 a 30 cm.", u"Remover el fondo del cantero y rellenar con materia orgánica."], 5),
        _create_mc_challenge(u"Las camas altas o canteros en una huerta, alcanzan un largo de:", [u"6 a 15 metros.", u"1 a 5 metros.", u"6 a 15 cm.", u"15 a 60 metros.", u"6 a 50 metros.", u"1 a 50 metros."], 5),
        _create_mc_challenge(u"En el tema de la huerta, el humus de lombriz se obtiene ulilizando lombrices para digerir:", [u"Materia orgánica.", u"Materia inorgánica.", u"Solo de excremento de animales.", u"Restos pino o eucaliptus.", u"Plásticos y vidrios.", u"Todos los residuos de la cocina."], 5),
        _create_mc_challenge(u"Para retirar el humus del lumbricario se debe:", [u"Separar las lombrices con trampas.", u"Esperar a que las lombrices se vayan solas.", u"Pasar el humus por filtros para atrapar las lombrices.", u"Poner productos para que la lombriz salga.", u"Mojar para espantar a las lombrices.", u"Quitar las lombrices con humo."], 6),
        _create_mc_challenge(u"¿Qué recomendaciones deberíamos cumplir cuando vamos a exponernos al sol?", [u"Usar protector solar.", u"Vestirnos con ropa blanca.", u"Tomar poca agua.", u"No es necesario usar gorro.", u"Tomar sol a las 12 hs. del mediodía.", u"No es necesario buscar lugares de sombra."], 6),
        _create_mc_challenge(u"¿Cuál de estas plantas se puede plantar con la arveja?", [u"Zanahoria.", u"Cebolla.", u"Ajo.", u"Papa.", u"Gladiolos.", u"Pino."], 6),
        _create_mc_challenge(u"Los canteros de la huerta se deben realizar de la siguiente manera:", [u"Separados por 50 cm.", u"Uno al lado del otro.", u"Separados por 6 metros.", u"Separados por 6 cm.", u"Sin separación.", u"A menos de 10 cm entre sí."], 6),
        _create_mc_challenge(u"Acerca de mis derechos y obligaciones en relación a mi salud la opción verdadera es:", [u"Todos los niños tenemos derecho a que los adultos responsables nos lleven a nuestros controles de salud.", u"Aprender a practicar hábitos saludables no es importante.", u"No es necesario que visite a mi doctor si no estoy viendo bien con mis ojos.", u"El olvidarme de mis controles de salud con el doctor no tiene importancia.", u"En mis controles de salud con el doctor, el control de mi peso y de mi altura no son importantes.", u"En mis controles de salud con el doctor no es importante que valoren cómo ven mis ojos."], 7),
        _create_mc_challenge(u"Cuando vamos a nadar a ríos o arroyos es importante:", [u"No nadar en contra de la corriente pues podemos cansarnos.", u"Tirarnos al agua aunque no sepamos nadar.", u"Comer antes de ir.", u"No llevar gorro.", u"Llevar alcohol.", u"Ir solos."], 7),
        _create_mc_challenge(u"Sobre nuestra huerta: ¿qué planta no es conveniente plantar con el pepino?", [u"Papa.", u"Girasol.", u"Porotos.", u"Maíz.", u"Arvejas.", u"Rabanito."], 7),
        _create_mc_challenge(u"Cuando se usan agroquímicos en la huerta: ", [u"No debemos mezclar la ropa contaminada con agroquímicos con ropa limpia.", u"No es importante usar ropa de protección específica para esa actividad.", u"Luego de haberlos aplicado, no es importante colgar en ambiente ventilado la vestimenta utilizada durante la aplicación.", u"No es necesario ducharse con abundante agua y jabón.", u"No es importante lavar la ropa contaminada con abundante agua y jabón.", u"No es necesario utilizar guantes durante el lavado de la ropa contaminada."], 7),
        _create_mc_challenge(u"¿Cuáles de estos síntomas deben tenerse en cuenta cuando usamos agroquímicos y consultar inmediatamente?", [u"Dificultad para respirar o falta de aire.", u"Risa.", u"Ganas de tomar un helado.", u"Ganas de leer.", u"Ganas de jugar a la Xo.", u"Ganas de ir a la escuela."], 8),
        _create_mc_challenge(u"¿Cuál de estas plantas en la huerta no se lleva bien con el resto de la lista?", [u"La Papa.", u"La Cebolla.", u"La Zanahoria.", u"La Menta.", u"La Ortiga.", u"La Borraja."], 8),
        _create_mc_challenge(u"¿Cuál de estos pasos no es necesario para comer alimentos crudos de la huerta?", [u"Hervir el alimento.", u"Potabilizar el agua en caso que no lo sea.", u"Sacar las partes en mal estado.", u"Eliminar restos de tierra con abundante agua potable.", u"Dejar en remojo 15 minutos con agua e hipoclorito.", u"Enjuagar nuevamente con abundante agua potable."], 8),
        _create_mc_challenge(u"¿Qué conoces acerca de los cuidados del sol?", [u"El sol emite radiaciones UV que pueden dañar seriamente nuestra piel.", u"El sol es recomendable a todas las horas del día.", u"El sol puede dañarnos más con ropa oscura que con ropa clara.", u"El sol es recomendable a las 2 de la tarde.", u"No es importante usar gorro cuando vamos a exponernos al sol.", u"No es necesario tomar agua cuando estoy al sol."], 8),
        _create_mc_challenge(u"En relación a los cuidados del sol:", [u"La piel de los niños es más fina y más propensa a sufrir los daños del sol a edades muy tempranas.", u"Es recomendable exponernos entre las 11 y las 17 horas.", u"Cuando vamos a exponernos al sol es importante usar ropa clara.", u"No es importante usar pantalla solar para protegernos del sol.", u"Los lentes de sol no son importantes porque los rayos UV no dañan los ojos.", u"Los lentes de sol solo deben ser usados por niños."], 9),
        _create_mc_challenge(u"¿Cuál de estas recomendaciones es la correcta al ir a bañarse? ", [u"Los niveles de profundidad en arroyos, bañados y lagos, cambian constantemente en función de los fenómenos climáticos.", u"Cuando vamos a estar al sol es recomendable usar ropa bien clara.", u"Es recomendable no tomar abundante agua.", u"Concurrir solos sin un adulto.", u"Tratar de comer por lo menos 15 minutos antes de ir a nadar.", u"Meternos al agua si no sabemos nadar."], 9),
        _create_mc_challenge(u"¿Qué recomendaciones debo conocer sobre los agroquímicos?", [u"No fumar, comer ni beber durante la manipulación de agroquímicos.", u"No es importante usar ropa de protección específica para usar agroquímicos.", u"No es importante colgar la vestimenta de protección utilizada durante la aplicación en un ambiente ventilado.", u"No es necesario lavar la ropa contaminada con abundante agua y jabón.", u"No es importante consultar al médico en caso de haber tenido contacto con una sustancia química y tener algún síntoma como falta de aire.", u"La correcta higiene de alimentos no es importante para evitar la contaminación con agroquímicos."], 9)
    ]
    return mc_challenges


def get_tf_challenges():
    
    # 0 = False | 1 = True
    tf_challenges = {}
    
    # Physica
    tf_challenges["physica"] = [
        _create_tf_challenge(u"Las vacunas son obligatorias en todos los niños porque refuerzan nuestro sistema inmunológico.", 1, 1),
        _create_tf_challenge(u"El ejercicio, disfrutar del tiempo libre, estar con amigos, reír, estar con la familia y estar de buen humor favorecen a que nuestro sistema inmune no se vea afectado.", 1, 1),
        _create_tf_challenge(u"Las vacunas no son importantes para nuestra salud.", 0, 1),
        _create_tf_challenge(u"Nuestro sistema inmune no mejora si nos alimentamos bien.", 0, 1),
        _create_tf_challenge(u"El estado de nuestro sistema inmune depende solo de lo que comemos.", 0, 1),
        _create_tf_challenge(u"La actividad física nos ayuda a prevenir enfermedades como el sobrepeso y la obesidad.", 1, 1),
        _create_tf_challenge(u"Los niños que no realizan actividad física tienen menos probabilidades de enfermarse.", 0, 1),
        _create_tf_challenge(u"Antes de empezar una actividad física, no es importante realizarnos controles médicos para saber cómo está nuestra salud.", 0, 1),
        _create_tf_challenge(u"Realizar actividad física no es tan importante como alimentarme saludablemente.", 0, 1),
        _create_tf_challenge(u"Cuando realizamos actividad física siempre es importante tomar agua para no deshidratarnos.", 1, 1),
        _create_tf_challenge(u"La actividad física no es parte de nuestra salud.", 0, 1),
        _create_tf_challenge(u"Solo los adultos deben realizar actividad física.", 0, 1),
        _create_tf_challenge(u"La alimentación adecuada previene muchas enfermedades importantes.", 1, 1),
        _create_tf_challenge(u"No solo los niños deben vacunarse, los adultos también.", 1, 1),
        _create_tf_challenge(u"Si realizo actividad física y me alimento de forma correcta, voy a lograr estar más sano.", 1, 1),
        _create_tf_challenge(u"Los niños que realizan actividad física tienen más probabilidades de enfermarse.", 0, 1),
        _create_tf_challenge(u"Si no nos vacunamos con las vacunas obligatorias podemos enfermarnos.", 1, 2),
        _create_tf_challenge(u"Recibir gratuitamente las vacunas obligatorias que figuran en el calendario de vacunas es un derecho de todos los niñas y niñas.", 1, 2),
        _create_tf_challenge(u"La actividad física no nos ayuda a prevenir enfermedades como el sobrepeso y la obesidad ", 0, 2),
        _create_tf_challenge(u"La actividad física ayuda a prevenir enfermedades.", 1, 2),
        _create_tf_challenge(u"La actividad física propicia una buena circulación a todo nuestro organismo.", 1, 2),
        _create_tf_challenge(u"Todas las veces que hagamos actividad física es muy importante tomar agua antes, durante y después de movernos.", 1, 2),
        _create_tf_challenge(u"Solo los niños deben realizar actividad física.", 0, 2),
        _create_tf_challenge(u"Nuestro sistema inmune no se afecta si trabajamos sin parar y descansamos poco.", 1, 3),
        _create_tf_challenge(u"Si realizo actividad física mi cuerpo se siente sano.", 1, 3),
        _create_tf_challenge(u"La actividad física ayuda a mantener nuestra salud.", 1, 3),
        _create_tf_challenge(u"La actividad física mejora la actividad de nuestro corazón.", 1, 3),
        _create_tf_challenge(u"Si no realizamos actividad física podemos llegar a tener enfermedades cardiovasculares.", 1, 3),
        _create_tf_challenge(u"Ser sedentarios no tiene importancia y no afecta nuestra salud.", 0, 4),
        _create_tf_challenge(u"Para que nuestro sistema inmune nos proteja debemos alimentarnos con frutas y verduras.", 1, 4),
        _create_tf_challenge(u"Hacer actividad física desde niños no previene enfermedades.", 0, 4),
        _create_tf_challenge(u"La actividad física no ayuda a prevenir enfermedades como la hipertensión arterial.", 0, 4),
        _create_tf_challenge(u"El sedentarismo no es un factor de riesgo para desarrollar enfermedades cardiovasculares.", 0, 5),
        _create_tf_challenge(u"Las personas que tuvieron un infarto al corazón no deben hacer actividad física.", 0, 5),
        _create_tf_challenge(u"Si no descansamos lo necesario nuestro sistema inmune puede perjudicarse.", 1, 5),
        _create_tf_challenge(u"Todos los niños y adolescentes tienen derecho a realizar actividad física para cuidar de su salud.", 1, 5),
        _create_tf_challenge(u"La actividad física ayuda a prevenir enfermedades como la diabetes.", 1, 5),
        _create_tf_challenge(u"Para no ser sedentarios debemos hacer actividad física por lo menos 5 días a la semana con una duración de al menos 30 minutos por día.", 1, 6),
        _create_tf_challenge(u"Si realizamos actividad física desde niños podemos prevenir enfermedades para cuando seamos más grandes.", 1, 6),
        _create_tf_challenge(u"Nuestro sistema inmune se verá afectado si no nos alimentamos correctamente.", 1, 6),
        _create_tf_challenge(u"La actividad física no es muy beneficiosa para nuestra salud.", 0, 6),
        _create_tf_challenge(u"La actividad física no nos ayuda a prevenir la osteoporosis.", 0, 7),
        _create_tf_challenge(u"Para evitar el sedentarismo, es conveniente no pasar más de dos horas diarias sentados frente a la televisión o la computadora.", 1, 7),
        _create_tf_challenge(u"Hacer actividad física desde niños no previene enfermedades.", 0, 7),
        _create_tf_challenge(u"Cuando estamos ingiriendo menos alimentos de los que necesitamos, nos volvemos menos susceptibles a las infecciones.", 0, 7),
        _create_tf_challenge(u"Las vacunas son obligatorias porque nos ayudan a desarrollar inmunidad y así prevenir enfermedades que pueden ser graves.", 1, 8),
        _create_tf_challenge(u"Las vacunas no refuerzan nuestro sistema inmune.", 0, 8),
        _create_tf_challenge(u"Las vacunas nos protegen de enfermedades y trabajan con nuestro sistema inmunológico.", 1, 8),
        _create_tf_challenge(u"Si aumenta el contenido de grasas en nuestra alimentación, podemos padecer enfermedades cardiovaculares", 1, 8),
        _create_tf_challenge(u"Las vacunas son obligatorias en todos los niños porque refuerzan nuestro sistema inmunológico.", 1, 9),
        _create_tf_challenge(u"Si descanso poco y trabajo en exceso mi sistema inmune puede verse perjudicado.", 1, 9),
        _create_tf_challenge(u"La actividad física no mejora nuestra imagen.", 0, 9),
        _create_tf_challenge(u"Existen vacunas que son obligatorias en todos los niños y niñas.", 1, 9)
    ]
    
    # Hygiene
    tf_challenges["hygiene"] = [
        _create_tf_challenge(u"El lavado de manos no es tan importante como una buena alimentación.", 0, 1),
        _create_tf_challenge(u"El primer paso al lavarnos las manos es ponernos jabón.", 0, 1),
        _create_tf_challenge(u"El primer paso al lavarnos las manos es mojarnos las manos con agua estancada.", 0, 1),
        _create_tf_challenge(u"Cuando lavo mis manos no es importante lavarme las uñas.", 0, 1),
        _create_tf_challenge(u"Después de sonar mi nariz no es importante lavar mis manos.", 0, 1),
        _create_tf_challenge(u"Después de tocar mascotas es muy importante lavar mis manos.", 1, 1),
        _create_tf_challenge(u"Después de ir al baño no es necesario lavar mis manos.", 0, 1),
        _create_tf_challenge(u"El alcohol en gel es tan eficaz como el lavado de manos con agua y jabón.", 0, 1),
        _create_tf_challenge(u"Es mejor usar alcohol en gel que agua y jabón.", 0, 1),
        _create_tf_challenge(u"Es muy importante aprender a cepillarnos los dientes.", 1, 1),
        _create_tf_challenge(u"Los dientes de leche no deben cepillarse.", 0, 1),
        _create_tf_challenge(u"Los bebés y los niños pequeños no necesitan ir al dentista.", 0, 1),
        _create_tf_challenge(u"Los dientes solo deben cepillarse una vez al día.", 0, 1),
        _create_tf_challenge(u"Los dientes deben cepillarse dos veces al día.", 0, 1),
        _create_tf_challenge(u"Los dientes deben cepillarse después de cada comida.", 1, 1),
        _create_tf_challenge(u"Después de sonar mi nariz es muy importante lavar mis manos.", 1, 1),
        _create_tf_challenge(u"Después de tocar mascotas no es importante lavar mis manos.", 0, 1),
        _create_tf_challenge(u"Las manos sólo deben lavarse cuando vamos a comer.", 0, 1),
        _create_tf_challenge(u"Aprender sobre salud bucal es cuidar nuestra salud.", 1, 1),
        _create_tf_challenge(u"Aprender el correcto cepillado de dientes no es importante.", 0, 1),
        _create_tf_challenge(u"Los bebés no necesitan ir al dentista porque no tienen dientes.", 0, 1),
        _create_tf_challenge(u"Debo ir al dentista por primera vez después que se caigan todos los dientes de leche.", 0, 1),
        _create_tf_challenge(u"Si solo como un caramelo o una golosina no es necesario cepillar mis dientes.", 0, 1),
        _create_tf_challenge(u"Es muy fácil aprender a cepillarnos los dientes.", 1, 1),
        _create_tf_challenge(u"Para que mis dientes sean fuertes y estén sanos tengo que alimentarme bien.", 1, 1),
        _create_tf_challenge(u"Después de jugar o hacer actividad física no es importante que nos lavemos las manos.", 0, 1),
        _create_tf_challenge(u"Cuando vengo de la escuela sólo debo lavarme las manos si voy a comer.", 0, 1),
        _create_tf_challenge(u"Muchos alimentos pueden estar contaminados con agroquímicos y pesticidas.", 1, 2),
        _create_tf_challenge(u"Aún cuando las manos se vean limpias, pueden tener gérmenes o microorganismos que causan enfermedades.", 1, 2),
        _create_tf_challenge(u"Las visitas al dentista son fundamentales para cuidar mi salud.", 1, 2),
        _create_tf_challenge(u"No es importante controlar el consumo de golosinas para cuidar nuestra salud bucal.", 0, 2),
        _create_tf_challenge(u"Para cuidar mis dientes no es importante controlar la cantidad de golosinas que como.", 0, 2),
        _create_tf_challenge(u"No solo mis dientes se enferman, también mis encías.", 1, 2),
        _create_tf_challenge(u"Para que mis dientes estén sanos no es importante comer frutas y verduras.", 0, 2),
        _create_tf_challenge(u"Si no cepillo mis dientes puedo adquirir caries.", 1, 2),
        _create_tf_challenge(u"Con las manos sucias podemos contaminar nuestros propios alimentos con microbios.", 1, 2),
        _create_tf_challenge(u"Los microbios en nuestras manos no son visibles a simple vista.", 1, 2),
        _create_tf_challenge(u"Es recomendable no tocarse los ojos, nariz o boca mientras se está en contacto con agroquímicos.", 1, 3),
        _create_tf_challenge(u"Después de jugar o venir de la escuela es importante que lave mis manos.", 1, 3),
        _create_tf_challenge(u"Al dentista puedo hacerle todas las preguntas que quiera en relación a mi salud bucal.", 1, 3),
        _create_tf_challenge(u"Los dientes deben cepillarse tres veces al día.", 0, 3),
        _create_tf_challenge(u"Al utilizar pasta dental no es importante que contenga flúor.", 0, 3),
        _create_tf_challenge(u"La caries no puede contagiarse de persona a persona.", 0, 3),
        _create_tf_challenge(u"No es importante alimentarse bien para que mis dientes estén sanos.", 0, 3),
        _create_tf_challenge(u"Cepillarse los dientes previene la invación de unos microorganismos que se llaman caries.", 1, 3),
        _create_tf_challenge(u"Las manos sólo deben lavarse cuando vamos a comer.", 0, 3),
        _create_tf_challenge(u"Si a mis manos no las veo sucias no es necesario que las lave.", 0, 3),
        _create_tf_challenge(u"Para evitar contaminarnos al utilizar agroquímicos, no es necesario usar ropa de protección.", 0, 4),
        _create_tf_challenge(u"El alcohol en gel debo usarlo siempre, aun si veo en mis manos suciedad.", 0, 4),
        _create_tf_challenge(u"Si voy al dentista puedo aprender a cuidar mis dientes y tener una linda sonrisa para reírme mucho.", 1, 4),
        _create_tf_challenge(u"Los dientes deben cepillarse cuatro veces al día.", 0, 4),
        _create_tf_challenge(u"Los niños más grandes pueden enseñar a los más pequeños sobre cómo deben cepillarse los dientes.", 1, 4),
        _create_tf_challenge(u"Si no me alimento bien, mis encías y dientes pueden enfermarse.", 1, 4),
        _create_tf_challenge(u"Es muy importante que en la escuela hablemos de cómo cuidar nuestros dientes.", 1, 4),
        _create_tf_challenge(u"Para que mis dientes estén sanos y fuertes no tengo que consumir alimentos ricos en flúor como pescados y espinaca.", 0, 4),
        _create_tf_challenge(u"Las manos deben lavarse solo dos veces al día.", 0, 4),
        _create_tf_challenge(u"El lavado de manos es una de las mejores medidas para prevenir enfermedades.", 1, 4),
        _create_tf_challenge(u"Cuando usamos agroquímicos es importante mantener separadas la ropa contaminada de la no contaminada.", 1, 5),
        _create_tf_challenge(u"Siempre es mejor un buen lavado de manos con agua y jabón que el uso de alcohol en gel.", 1, 5),
        _create_tf_challenge(u"Tener una sonrisa linda con mis dientes sanos es muy agradable.", 1, 5),
        _create_tf_challenge(u"Es muy importante cepillar mis dientes después de cada comida.", 1, 5),
        _create_tf_challenge(u"Los dientes de leche no deben cepillarse.", 0, 5),
        _create_tf_challenge(u"Si mis dientes o encías están enfermos puedo tener mal aliento.", 1, 5),
        _create_tf_challenge(u"Es importante hablar de cómo cuidar nuestros dientes con nuestros amigos.", 1, 5),
        _create_tf_challenge(u"Si un diente es arrancado por un golpe, tenemos que ponerlo rápidamente en leche o agua fría y llevarlo al dentista inmediatamente.", 1, 5),
        _create_tf_challenge(u"Las manos deben lavarse 3 veces al día.", 0, 5),
        _create_tf_challenge(u"Si no voy a comer no necesito lavarme las manos.", 0, 5),
        _create_tf_challenge(u"En caso de tener contacto con una sustancia química y manifestar algún síntoma como ardor ocular, hay que lavar con abundante agua y consultar al médico lo más rápido posible.", 1, 6),
        _create_tf_challenge(u"Es recomendable que visite al dentista por lo menos cada 6 meses.", 1, 6),
        _create_tf_challenge(u"Mis controles con el odontólogo o dentista no son tan importantes como los controles en salud con mi doctor.", 0, 6),
        _create_tf_challenge(u"No es necesario cepillar mis dientes cada vez que ingiero comida.", 0, 6),
        _create_tf_challenge(u"Yo tengo derecho a que controlen mis dientes para saber cómo está mi salud.", 1, 6),
        _create_tf_challenge(u"El mal aliento no puede ser porque mis dientes o encías estén enfermos.", 0, 6),
        _create_tf_challenge(u"No es importante hablar sobre cómo cuidar nuestros dientes.", 0, 6),
        _create_tf_challenge(u"Antes de comer es muy importante que lavemos nuestras manos con agua y jabón.", 1, 6),
        _create_tf_challenge(u"Las manos deben lavarse 4 veces al día.", 0, 6),
        _create_tf_challenge(u"El lavado de manos, cuando se realiza en forma correcta, es la manera más eficaz de prevenir la trasmisión de enfermedades.", 1, 7),
        _create_tf_challenge(u"Es recomendable que visite al dentista una vez cada dos años.", 0, 7),
        _create_tf_challenge(u"Tener una sonrisa saludable es parte de nuestra salud.", 1, 7),
        _create_tf_challenge(u"No es importante cepillar mis dientes cada vez que como.", 0, 7),
        _create_tf_challenge(u"Los dientes deben cepillarse con pasta de dientes y no con otros productos.", 1, 7),
        _create_tf_challenge(u"Para que mis dientes estén sanos y fuertes tengo que comer quesos, leche o yogurt, porque son alimentos que contienen calcio.", 1, 7),
        _create_tf_challenge(u"Hay muchos alimentos que favorecen la aparición de caries.", 1, 7),
        _create_tf_challenge(u"Lavándonos las manos no eliminamos microbios que pueden afectar nuestra salud.", 0, 7),
        _create_tf_challenge(u"Después de practicar deportes debemos lavarnos las manos.", 1, 7),
        _create_tf_challenge(u"El primer paso al lavarnos las manos es mojarlas con agua corriente.", 1, 8),
        _create_tf_challenge(u"Es recomendable que visite el dentista sólo cuando me duele un diente o una muela.", 0, 8),
        _create_tf_challenge(u"Para tener salud bucal es muy importante controlar el consumo de azúcar.", 1, 8),
        _create_tf_challenge(u"Si mis dientes están sanos me siento más contento y me veo mejor.", 1, 8),
        _create_tf_challenge(u"Para que mis dientes estén sanos tengo que comer muchas frutas y verduras.", 1, 8),
        _create_tf_challenge(u"Con el cepillado de dientes no puedo prevenir la aparición de caries.", 0, 8),
        _create_tf_challenge(u"Con las manos sucias podemos contagiarnos de enfermedades.", 1, 8),
        _create_tf_challenge(u"Las manos son una de las partes del cuerpo que menos microbios poseen.", 0, 8),
        _create_tf_challenge(u"Bañarnos todos los días con agua y jabón también es cuidar nuestra salud y es muy importante.", 1, 9),
        _create_tf_challenge(u"Los dientes de leche también deben cepillarse.", 1, 9),
        _create_tf_challenge(u"Para tener dientes sanos no debo comer demasiadas golosinas.", 1, 9),
        _create_tf_challenge(u"El cigarrillo no afecta la salud de los dientes.", 0, 9),
        _create_tf_challenge(u"El cigarrillo afecta la salud de los dientes.", 1, 9),
        _create_tf_challenge(u"Los microbios en nuestras manos son visibles a simple vista.", 0, 9)
    ]
    
    # REVISADO HASTA ACÁ
    
    # Nutrition
    tf_challenges["nutrition"] = [
        _create_tf_challenge(u"Cuando aprendemos hábitos saludables no estamos cuidando nuestra salud.", 0, 1),
        _create_tf_challenge(u"Tomar mucha agua, comer frutas y verduras y hacer ejercicio no ayuda a mover el intestino sin dificultad.", 0, 1),
        _create_tf_challenge(u"El acceso a la salud y a una alimentación saludable es un derecho de todos.", 1, 1),
        _create_tf_challenge(u"No todos tenemos derecho a alimentarnos saludablemente.", 0, 1),
        _create_tf_challenge(u"El desayuno no es importante en nuestra alimentación.", 0, 1),
        _create_tf_challenge(u"La alimentación diaria debe ser variada y muy rica en grasas.", 0, 1),
        _create_tf_challenge(u"Las grasas saturadas las encontramos en: jamones, embutidos, manteca, margarina y varios cortes de carne de vaca, cordero y cerdo.", 1, 1),
        _create_tf_challenge(u"Se recomienda a niños y adolescentes consumir entre 2 y 3 porciones diarias de grasas y aceites.", 1, 1),
        _create_tf_challenge(u"Se recomienda a niños y adolescentes consumir entre 4 y 5 porciones diarias de azúcares de dulces.", 1, 1),
        _create_tf_challenge(u"Los alimentos en su forma natural ya contienen sal y agregar mucha sal a los mismos perjudica nuestra salud cardiovascular.", 1, 1),
        _create_tf_challenge(u"Los alimentos no tienen sal a menos que se le agruege.", 0, 1),
        _create_tf_challenge(u"El agua es el principal e imprescindible componente del cuerpo humano.", 1, 1),
        _create_tf_challenge(u"Necesitamos consumir entre 2 a 3 litros por día de agua.", 1, 1),
        _create_tf_challenge(u"Se recomienda a niños y adolescentes consumir entre 5 y 7 porciones diarias de cereales y leguminosas.", 1, 1),
        _create_tf_challenge(u"Se recomienda a niños y adolescentes consumir entre 2 y 3 porciones de frutas y verduras.", 0, 1),
        _create_tf_challenge(u"Se recomienda a niños y adolescentes consumir 2 porciones diarias de leches y derivados.", 1, 1),
        _create_tf_challenge(u"Los niños deben consumir aproximadamente uno litro y medio de leche por día.", 0, 1),
        _create_tf_challenge(u"Se recomienda a niños y adolescentes consumir 2 o 3 porciones diarias de carnes derivados y huevos.", 1, 1),
        _create_tf_challenge(u"La carne, fiambres, huevos, leche y manteca, deben ser almacenados en heladera.", 1, 1),
        _create_tf_challenge(u"Debemos tratar de no guardar en el mismo recipiente alimentos cocidos con alimentos crudos.", 1, 1),
        _create_tf_challenge(u"Las frutas y verduras se conservaran en la heladera envueltas en bolsa de plástico limpias o en recipientes cerrados.", 1, 1),
        _create_tf_challenge(u"Es recomendable congelar un alimento que ya fue descongelado.", 0, 1),
        _create_tf_challenge(u"Si tenemos mascotas debemos mantenerlas lejos de nuestros alimentos.", 1, 1),
        _create_tf_challenge(u"Las grasas no cumplen funciones en nuestro organismo.", 0, 1),
        _create_tf_challenge(u"La fibra alimentaria no regula funciones intestinales.", 0, 2),
        _create_tf_challenge(u"El consumo de fibras no es importante para regular nuestros niveles de colesterol.", 0, 2),
        _create_tf_challenge(u"Si consumimos muchos alimentos que contienen grasas evitamos tener enfermedades cardiovasculares.", 0, 2),
        _create_tf_challenge(u"Las vitaminas son nutrientes que son vitales para nuestro organismo.", 1, 2),
        _create_tf_challenge(u"Al practicar ejercicio físico debemos aumentar nuestro consumo de agua.", 1, 2),
        _create_tf_challenge(u"La contaminación cruzada es el pasaje de microbios de un alimento a crudo a otro cocido listo para consumir.", 1, 2),
        _create_tf_challenge(u"No debemos consumir huevos poco cocidos, mayonesas caseras o merengues crudos, por el peligro de padecer una enfermedad que se llama salmonelosis.", 1, 2),
        _create_tf_challenge(u"Las fibras ayudan a regular la movilidad intestinal.", 1, 3),
        _create_tf_challenge(u"El consumo de fibras nos ayuda a movilizar nuestro intestino sin dificultad.", 1, 3),
        _create_tf_challenge(u"A medida que aumenta el contenido de grasas en la alimentación de las personas, aumenta la probabilidad de padecer problemas cardiovasculares", 1, 3),
        _create_tf_challenge(u"Si a las verduras las dejamos hervir durante mucho tiempo el contenido de las vitaminas será mejor.", 0, 3),
        _create_tf_challenge(u"Manipular los alimentos de una forma higiénica no es importante para evitar la contaminación por microbios o sustancias tóxicas que pueden producirnos enfermedades.", 0, 3),
        _create_tf_challenge(u"Antes de manipular los alimentos, después de prepararlos y antes de consumirlos, debemos lavarnos las manos por lo menos durante 30 segundos.", 1, 3),
        _create_tf_challenge(u"No es recomendable congelar un alimento que ya fue descongelado.", 1, 3),
        _create_tf_challenge(u"Los alimentos ricos en fibras no ayudan a que movilicemos nuestro intestino sin problemas.", 0, 4),
        _create_tf_challenge(u"Se recomienda comer frutas, verduras, hortalizas, legumbres y cereales integrales que tienen un alto contenido de fibras.", 1, 4),
        _create_tf_challenge(u"Las vitaminas son nutrientes que no son importantes.", 0, 4),
        _create_tf_challenge(u"Si cocinamos las verduras en una olla a presión o al vapor, se pierden más vitaminas.", 0, 4),
        _create_tf_challenge(u"Cuando guardamos harinas, fideos secos o azúcar debemos hacerlo en lugares cerrados, protegidos de insectos y roedores.", 1, 4),
        _create_tf_challenge(u"Cuando manipulamos carnes o huevos, no es necesario lavar con agua caliente y jabón todos los utensilios de cocina que utilizamos incluso la tabla de picar los alimentos.", 0, 4),
        _create_tf_challenge(u"Debemos consumir leche pasteurizada, y si no tenemos acceso a ella, debemos siempre hervirla antes de consumirla.", 1, 4),
        _create_tf_challenge(u"Cuando ingerimos grandes cantidades de grasas saturadas, estamos aumentando la probabilidad de padecer enfermedades cardiovasculares.", 1, 5),
        _create_tf_challenge(u"El consumo de proteínas adecuado nos permite tener uñas y cabellos fuertes.", 1, 5),
        _create_tf_challenge(u"Las deficiencias de vitaminas y los excesos de algunas de ellas provocan enfermedades.", 1, 5),
        _create_tf_challenge(u"El contenido de vitaminas de los alimentos no se ve influenciado por el modo en que los cocinemos.", 0, 5),
        _create_tf_challenge(u"Podemos guardar alimentos junto a productos químicos como insecticidas, productos de limpieza y venenos.", 0, 5),
        _create_tf_challenge(u"Al guardar alimentos junto a insecticidas, productos de limpieza o venenos, pueden contaminarse y ser muy perjudiciales para nuestra salud.", 1, 5),
        _create_tf_challenge(u"Las frutas y verduras deben ser lavadas cuidadosamente con agua de la canilla, jabón e hipoclorito de sodio.", 1, 5),
        _create_tf_challenge(u"Hervir la leche que no es pasteurizada no tiene importancia.", 0, 5),
        _create_tf_challenge(u"Los alimentos son sustancias químicas contenidas en los nutrientes.", 0, 6),
        _create_tf_challenge(u"Cuando ingerimos pequeñas cantidades de grasas saturadas, estamos aumentando la probabilidad de padecer enfermedades cardiovasculares.", 0, 6),
        _create_tf_challenge(u"Cuando consumimos grandes cantidades de grasas saturadas estamos aumentando la probabilidad de padecer muchas enfermedades cardiovasculares.", 1, 6),
        _create_tf_challenge(u"El agua permite el transporte de nutrientes a las células.", 1, 6),
        _create_tf_challenge(u"No es importante mantener las carnes crudas separadas de otros alimentos.", 0, 6),
        _create_tf_challenge(u"Los alimentos como carnes y derivados deben colocarse en heladera lo más rápidamente posbile luego de comprados.", 1, 6),
        _create_tf_challenge(u"Las proteínas están formadas por unas unidades básicas llamadas aminoácidos.", 1, 7),
        _create_tf_challenge(u"Las proteínas se encuentran principalmente en alimentos de origen animal (leche y derivados, carne, pollo, pescado, huevos, etc).", 1, 7),
        _create_tf_challenge(u"Una cantidad limitada de colesterol es necesaria en nuestro organismo, pero en exceso puede generar problemas cardiovasculares.", 1, 7),
        _create_tf_challenge(u"El consumo de alimentos ricos en calcio es imprescindible solo en los niños pequeños.", 0, 7),
        _create_tf_challenge(u"Si vamos a descongelar alimentos debemos colocarlos primero en la heladera y no descongelarlos a temperatura ambiente.", 1, 7),
        _create_tf_challenge(u"Las cáscaras de las frutas son ricas en vitaminas.", 1, 7),
        _create_tf_challenge(u"Es muy importante consumir alimentos ricos en calcio durante toda la vida.", 1, 7),
        _create_tf_challenge(u"Los azúcares, proteínas y grasas son llamados micronutrientes.", 0, 8),
        _create_tf_challenge(u"El colesterol bueno o HDL tiene un rol protector a diferencia del colesterol LDL o colesterol malo.", 1, 8),
        _create_tf_challenge(u"Las grasas saturadas son las grasas que aumentan el colesterol bueno o HDL.", 0, 8),
        _create_tf_challenge(u"El consumo de alimentos ricos en calcio es muy importante.", 0, 8),
        _create_tf_challenge(u"Una buena manera de poder conservar las vitaminas de los alimentos es cocinándolos con una olla a presión o al vapor.", 1, 8),
        _create_tf_challenge(u"Las cáscaras de las frutas no son ricas en vitaminas.", 0, 8),
        _create_tf_challenge(u"Las vitaminas y minerales son llamados macronutrientes.", 0, 9),
        _create_tf_challenge(u"El colesterol LDL es conocido como el colesterol “MALO” es el que se acumula en las arterias ocluyéndolas teniendo un efecto contrario al colesterol HDL o “BUENO”.", 1, 9),
        _create_tf_challenge(u"Consumir alimentos ricos en calcio es imprescindible en todas las etapas de la vida para disminuir la probabilidad de contraer la enfermedad osteoporosis cuando seamos adultos.", 1, 9),
        _create_tf_challenge(u"La leche y los quesos son ricos en calcio.", 1, 9),
        _create_tf_challenge(u"Las vitaminas se conservan de igual forma en las verduras independientemente de si las cocinamos al vapor o las hervimos.", 0, 9),
        _create_tf_challenge(u"Cuando manipulamos carnes o huevos, debemos lavar con agua caliente y jabón todos los utensilios de cocina que utilizamos incluso la tabla de picar los alimentos.", 1, 9),
        _create_tf_challenge(u"El agua posibilita el transporte de nutrientes a las células y de las sustancias de desecho desde las células.", 1, 9)
    ]
    
    # Spare time
    tf_challenges["spare_time"] = [            
        _create_tf_challenge(u"Sólo se debe realizar actividad física en la escuela.", 0, 1),
        _create_tf_challenge(u"La actividad física nos pone de mal humor.", 0, 1),
        _create_tf_challenge(u"Es muy saludable hacer actividad física con mi familia porque todos aprendemos a cuidar de nuestra salud.", 1, 1),
        _create_tf_challenge(u"Las actividades físicas son aburridas porque son pocas.", 0, 1),
        _create_tf_challenge(u"Debemos realizar actividad física todos los días.", 1, 1),
        _create_tf_challenge(u"El descanso después de hacer ejercicio no es importante.", 0, 1),
        _create_tf_challenge(u"Cuando bailamos no estamos haciendo actividad física.", 0, 1),
        _create_tf_challenge(u"El tiempo libre y la recreación no forman parte de nuestra salud.", 0, 1),
        _create_tf_challenge(u"Podemos realizar actividad física de formas muy variadas y divertidas.", 1, 1),
        _create_tf_challenge(u"Es recomendable preguntar qué actividad física podemos hacer a nuestra edad.", 1, 2),
        _create_tf_challenge(u"La actividad física disminuye el estrés y alivia tensiones.", 1, 2),
        _create_tf_challenge(u"Podemos realizar actividad física mientras jugamos en la escuela y nos movemos.", 1, 2),
        _create_tf_challenge(u"La actividad física puede volverse muy divertida porque es muy variada.", 1, 3),
        _create_tf_challenge(u"Si trabajamos sin parar, estudiamos sin parar, dormimos pocas horas, no descansamos o estamos estresados, corremos el riesgo de enfermar.", 1, 3),
        _create_tf_challenge(u"La actividad física nos permite además de hacer ejercicio compartir momentos agradables con mis compañeros.", 1, 4),
        _create_tf_challenge(u"Es recomendable realizar como mínimo 30 minutos de actividad física dos veces en la semana.", 0, 4),
        _create_tf_challenge(u"Realizando actividad física podemos divertirnos, recrearnos, reírnos y conocernos.", 1, 5),
        _create_tf_challenge(u"Todos los niños y adolescentes tienen derecho a realizar actividad física para cuidar de su salud.", 1, 5),
        _create_tf_challenge(u"La actividad física ayuda a estar de buen humor.", 1, 6),
        _create_tf_challenge(u"La actividad física no nos permite descansar mejor.", 0, 6),
        _create_tf_challenge(u"La actividad física me permite estar en contacto con la naturaleza y a su vez conocerla.", 1, 7),
        _create_tf_challenge(u"La actividad física hace “verme mejor”.", 1, 7),
        _create_tf_challenge(u"Es recomendable realizar todos los días 30 minutos de actividad física.", 1, 8),
        _create_tf_challenge(u"La recreación, la diversión y el disfrute del tiempo libre, aportan de manera muy positiva a nuestra calidad de vida.", 1, 8),
        _create_tf_challenge(u"Realizar actividad física 10 minutos por día es suficiente para estar sanos.", 0, 9),
        _create_tf_challenge(u"Es importante tomarnos un momento del día para hacer actividades que nos agraden y nos permita reir, compartir, estar con amigos y recrearnos.", 1, 9)
    ]
    
    # Responsability
    tf_challenges["responsability"] = [
        _create_tf_challenge(u"Si estoy sano, no tengo que ir al doctor.", 0, 1),
        _create_tf_challenge(u"Cuando no me duele nada no es necesario ir al doctor.", 0, 1),
        _create_tf_challenge(u"A mi edad debo ir al doctor todas las semanas.", 0, 1),
        _create_tf_challenge(u"A mi edad debo ir al doctor dos veces al mes.", 0, 1),
        _create_tf_challenge(u"A mi edad debo ir a controlarme por lo menos una vez al año.", 1, 1),
        _create_tf_challenge(u"En mis controles de salud me pesan y miden mi altura, para asegurarse de que estoy creciendo bien.", 1, 1),
        _create_tf_challenge(u"Debo ir al doctor solo cuando estoy enfermo.", 0, 1),
        _create_tf_challenge(u"Solo niños deben controlar su salud aunque estén sanos.", 0, 1),
        _create_tf_challenge(u"Las vacunas son obligatorias porque nos ayudan a desarrollar inmunidad y así prevenir enfermedades que pueden ser graves.", 1, 1),
        _create_tf_challenge(u"Cuidar nuestra salud es una responsabilidad que todos los niños tenemos que aprender.", 1, 1),
        _create_tf_challenge(u"Mis visitas al doctor y mis controles ayudan a mantenerme sano.", 1, 1),
        _create_tf_challenge(u"No solo los niños deben vacunarse, los adultos también.", 1, 1),
        _create_tf_challenge(u"Si no me llevan al doctor, debo pedir que me lleven porque tengo derecho a controlarme.", 1, 1),
        _create_tf_challenge(u"En mis controles de salud, es muy importante que controlen cómo “veo” y cómo están mis ojos.", 1, 1),
        _create_tf_challenge(u"Solo debo ir al doctor cuando estoy enfermo.", 0, 1),
        _create_tf_challenge(u"En mis controles de salud es importante que examinen mi piel para ver si no tengo alguna enfermedad provocada por el sol.", 1, 1),
        _create_tf_challenge(u"En mis controles de salud no es importante que controlen como “veo” y cómo están mis ojos.", 0, 1),
        _create_tf_challenge(u"Cuando voy a mis controles de salud no es importante que revisen mi cuerpo.", 0, 1),
        _create_tf_challenge(u"No tengo que tener miedo de ir al doctor porque los doctores protegen nuestra salud y nos ayudan a aprender a cuidarnos.", 1, 1),
        _create_tf_challenge(u"Tener mi carné de vacunas al día es cuidar de nuestra salud.", 1, 1),
        _create_tf_challenge(u"Cualquier lesión que nos salga en la piel y nos llame la atención es recomendable que sea vista por un médico.", 1, 1),
        _create_tf_challenge(u"Si vamos a exponernos al sol es recomendable que la ropa sea oscura.", 1, 1),
        _create_tf_challenge(u"Si vamos a exponernos al sol es recomendable buscar espacios de sombra.", 1, 1),
        _create_tf_challenge(u"Si vamos a exponernos al sol es recomendable usar gorro de ala ancha o que proteja cara, orejas y cuello.", 1, 1),
        _create_tf_challenge(u"Si vamos a exponernos al sol no es importante consumir abundantes líquidos.", 0, 1),
        _create_tf_challenge(u"Una piel hidratada siempre nos protege mejor del sol.", 1, 1),
        _create_tf_challenge(u"El uso de lentes de sol y protectores solares no es necessario cuando nos exponemos al sol.", 0, 1),
        _create_tf_challenge(u"Los rayos UV pueden dañar nuestra piel pero no nuestros ojos.", 0, 1),
        _create_tf_challenge(u"Si no se nadar es recomendable que no me meta al agua sin el acompañamiento de un adulto.", 1, 1),
        _create_tf_challenge(u"No es necesario que si voy a estar al sol me proteja la piel con ropa adecuada.", 0, 1),
        _create_tf_challenge(u"Si no nos protegemos del sol la piel puede ser seriamente dañada.", 1, 1),
        _create_tf_challenge(u"En mis controles en salud con el doctor puedo aprender muchas cosas y después compartirlas en mi familia o en la escuela con mis maestras y mis compañeros.", 1, 2),
        _create_tf_challenge(u"Los niños son los únicos que deben visitar al doctor aunque estén sanos.", 0, 2),
        _create_tf_challenge(u"Es muy importante tener nuestro carné de vacunas al día.", 1, 2),
        _create_tf_challenge(u"En mis controles en salud es indispensable que el doctor examine mi cuerpo para ver cómo estamos creciendo y desarrollandonos.", 1, 2),
        _create_tf_challenge(u"Todos los niños y niñas tienen derecho a que los lleven a controles en salud con el doctor.", 1, 2),
        _create_tf_challenge(u"Si vamos a exponernos al sol, es recomendable que la ropa sea oscura y además que cubra hombros, brazos y piernas.", 1, 2),
        _create_tf_challenge(u"Se puede cosechar todas las plantas sin pensar en la cantidad que vamos a consumir.", 0, 2),
        _create_tf_challenge(u"Las camas altas de la huerta pueden llegar a medir 1 metro de ancho y hasta 15 metros de largo.", 1, 2),
        _create_tf_challenge(u"En la nuerta se debe realizar una canaleta rodeando la cama alta para que el agua corra.", 1, 2),
        _create_tf_challenge(u"En una huerta, el mantenimiento y control de plagas es tan importante como la siembra.", 1, 2),
        _create_tf_challenge(u"En la huerta, es muy importante llevar registro de los cultivos y los cuidados necesarios, para próximas siembras.", 1, 2),
        _create_tf_challenge(u"Si en una huerta se siembra más de una variedad, debemos colocar las de menor tamaño al centro y las de mayor al costado del cantero.", 0, 2),
        _create_tf_challenge(u"Cuando en una huerta se utilizan almácigos es más fácil cuidar las semillas que usando siembra directa.", 1, 2),
        _create_tf_challenge(u"En mis controles en salud puedo aprender muchas cosas nuevas acerca de mi salud.", 1, 3),
        _create_tf_challenge(u"A mi edad debo ir al doctor todos los meses.", 0, 3),
        _create_tf_challenge(u"No es importante tener nuestro carné de vacunas al día.", 0, 3),
        _create_tf_challenge(u"Al doctor puedo hacerle todas las preguntas que quiera sobre mi salud.", 1, 3),
        _create_tf_challenge(u"Los controles en salud no son importantes y no ayudan a sacarme las dudas.", 0, 3),
        _create_tf_challenge(u"Si vamos a estar al sol debemos tomar mucha agua.", 1, 3),
        _create_tf_challenge(u"Al cosechar no debemos dañar la planta porque es vía de entrada de microbios.", 1, 3),
        _create_tf_challenge(u"Entre las camas altas de una huerta no es necesario dejar caminos intermedios para circular.", 0, 3),
        _create_tf_challenge(u"El único método de sembrar en una huerta, es de manera directa en los canteros.", 0, 3),
        _create_tf_challenge(u"En la huerta los almácigos constituyen un microclima controlado, por lo tanto no es importante mantenerlos libres de yuyos.", 0, 3),
        _create_tf_challenge(u"Antes de sembrar debemos estudiar qué plantas son compañeras y cuales no, para que no se perjudiquen entre si.", 1, 3),
        _create_tf_challenge(u"Los controles en salud no son importantes.", 0, 4),
        _create_tf_challenge(u"En mis controles en salud no aprendo cosas nuevas.", 0, 4),
        _create_tf_challenge(u"Es muy importante que el doctor revise mi carné de vacunas para asegurarnos de que estamos bien vacunados.", 1, 4),
        _create_tf_challenge(u"Si no siento dolor no tengo porque ir al doctor.", 0, 4),
        _create_tf_challenge(u"Poder cuidar de nuestra salud es un derecho que tenemos todos.", 1, 4),
        _create_tf_challenge(u"Cuando vamos al agua es importante estar en lugares del agua donde damos pie y en lo posible con el agua hasta la cintura.", 1, 4),
        _create_tf_challenge(u"Al cosechar se pueden cortar las hojas, frutos, o la parte que corresponda sin tener mucho cuidado.", 0, 4),
        _create_tf_challenge(u"La profundidad de la cama alta puede llegar hasta 6 metros.", 0, 4),
        _create_tf_challenge(u"Además de la siembra directa, podemos hacerlo en almácigos.", 1, 4),
        _create_tf_challenge(u"Al realizar un almácigo debemos preparar la tierra con buena cantidad de materia orgánica.", 1, 4),
        _create_tf_challenge(u"Antes de cosechar debemos limpiar los utensilios para evitar enfermar a la planta.", 1, 4),
        _create_tf_challenge(u"Es conveniente sembrar juntas plantas de la misma familia botánica (ejemplo: morrón y tomate).", 0, 4),
        _create_tf_challenge(u"Los controles en salud son muy importantes para todas las personas.", 1, 5),
        _create_tf_challenge(u"Los controles médicos no son importantes.", 0, 5),
        _create_tf_challenge(u"No es importante que me pesen y midan mi altura cuando voy a mis controles en salud con el doctor.", 0, 5),
        _create_tf_challenge(u"Los niños más pequeños se controlan con menor frecuencia que los adultos.", 0, 5),
        _create_tf_challenge(u"Existen vacunas que son obligatorias en todos los niños y niñas.", 1, 5),
        _create_tf_challenge(u"Cuando vamos al agua es fundamental que un adulto nos acompañe y que no vayamos solos.", 1, 5),
        _create_tf_challenge(u"Al cosechar en la huerta, debemos quitar los restos de cultivos enfermos de los canteros.", 1, 5),
        _create_tf_challenge(u"Al sacar la tierra de la cama alta de la huerta, debo deshacerme de ella, ya que no sirve para nada más en mi huerta.", 0, 5),
        _create_tf_challenge(u"Las formas de siembra en almácigos son: en línea, al voleo y en casilla o hueco.", 0, 5),
        _create_tf_challenge(u"Cuando la huerta recibe abundante lluvia debemos retirar el agua de los canteros.", 1, 5),
        _create_tf_challenge(u"Cuando en la huerta aparecen plagas, enfermedades o malezas podemos combatirlas con agroquímicos.", 0, 5),
        _create_tf_challenge(u"En la huerta conviene hacer las camas altas y canteros con una orientación Este-Oeste, a la sombra y en un lugar inundable.", 0, 5),
        _create_tf_challenge(u"Los niños más pequeños se controlan en salud con mayor frecuencia que los más grandes.", 1, 6),
        _create_tf_challenge(u"No es necesario ir al doctor cuando nos sentimos sanos.", 0, 6),
        _create_tf_challenge(u"La frecuencia de controles en salud no depende de la edad de los niños.", 0, 6),
        _create_tf_challenge(u"Debo ir al doctor sólo cuando me siento enfermo.", 0, 6),
        _create_tf_challenge(u"No es importante que en mis controles de salud el doctor revise mi carné de vacunas.", 0, 6),
        _create_tf_challenge(u"Esta bien si vamos al agua solos.", 0, 6),
        _create_tf_challenge(u"Podemos cosechar sin importar el tiempo que tiene de siembra.", 0, 6),
        _create_tf_challenge(u"La tierra que saco de la cama alta, luego se reutiliza ya que es tierra limpia.", 1, 6),
        _create_tf_challenge(u"Luego de sembrar, tan sólo debemos esperar a que este lista la cosecha.", 0, 6),
        _create_tf_challenge(u"Cualquier tipo de agua nos sirve para regar la huerta, sin importar de donde viene.", 0, 6),
        _create_tf_challenge(u"Los sapos y las ranas son perjudiciales para el desarrollo de la huerta.", 0, 6),
        _create_tf_challenge(u"El humus de lombriz se obtiene utilizando lombrices para digerir la materia inorgánica.", 0, 6),
        _create_tf_challenge(u"Los controles en salud son una oportunidad para poder aprender sobre mi salud y sacarme las dudas que tenga en relación a la misma.", 1, 7),
        _create_tf_challenge(u"Cuando voy a los controles en salud es muy importante que el doctor examine mi cuerpo para ver si estoy sano.", 1, 7),
        _create_tf_challenge(u"Cuando voy al doctor a controlarme, me toman la presión arterial en el brazo para ver como estoy y asegurarme de que estoy bien.", 1, 7),
        _create_tf_challenge(u"Si concurro a mis controles en salud aprendo a evitar enfermarme.", 1, 7),
        _create_tf_challenge(u"En la huerta debemos cosechar en el momento adecuado.", 1, 7),
        _create_tf_challenge(u"Cualquier tipo de suelo nos sirve para realizar nuestra huerta.", 0, 7),
        _create_tf_challenge(u"Los canteros deben ser profundos para que se inunde de agua de lluvia.", 0, 7),
        _create_tf_challenge(u"Se recomienda colocar flores olorosas y de colores vivos para estimular la presencia de enemigos naturales de las plagas.", 1, 7),
        _create_tf_challenge(u"El humus provee de elementos nutritivos al suelo y mejora la retención de aire y agua en el suelo.", 1, 7),
        _create_tf_challenge(u"La toma de presión arterial en mis controles con el doctor es muy importante para poder evaluar como estoy y poder darnos cuenta a tiempo de una posible hipertensión arterial.", 1, 8),
        _create_tf_challenge(u"A mi edad lo recomendable es que visite al doctor por lo menos una vez al año.", 1, 8),
        _create_tf_challenge(u"Es recomendable exponernos al sol durante las horas 11:00 y 17:00 del día, pues es en esas horas donde el riesgo de daño es menor.", 0, 8),
        _create_tf_challenge(u"Los niveles de profundidad en arroyos, bañados y lagos cambian constantemente en función de los fenómenos climáticos por eso debemos ser muy cuidadodos.", 1, 8),
        _create_tf_challenge(u"Luego de elegido el terreno para la huerta, debemos limpiar la superficie, sacando piedras, vidrios y basura.", 1, 8),
        _create_tf_challenge(u"Los canteros de la huerta deben quedar más alto en el medio que en los bordes.", 1, 8),
        _create_tf_challenge(u"Para mejorar la calidad del control natural de plagas se recomienda tener la máxima diversidad de plantas en la huerta.", 1, 8),
        _create_tf_challenge(u"La formación de abono orgánico es el resultado de la transformación de residuos orgánicos en materia por acción de diversos organismos.", 1, 8),
        _create_tf_challenge(u"En nuestro país y en el mundo muchas personas tienen presión arterial elevada y por eso desde niños tenemos que controlarnos la presión arterial.", 1, 9),
        _create_tf_challenge(u"Si vamos a exponernos al sol, es recomendable que la ropa sea blanca.", 0, 9),
        _create_tf_challenge(u"Si vamos a disfrutar del agua a un río, arroyo o piscina y llevamos gomones o juegos inflables de agua, es muy importante atarlos fuertemente a un árbol o rama gruesa.", 1, 9),
        _create_tf_challenge(u"Cuando la tierra de la huerta está preparada, podemos plantar cualquier semilla sin importar la época del año en que estamos.", 0, 9),
        _create_tf_challenge(u"El cantero debe quedar más bajo en el medio que en los bordes.", 0, 9),
        _create_tf_challenge(u"Para consumir crudos los alimentos debemos sacar las partes en mal estado, sacar resto de tierra, remojar y enjuagarlos con abundante agua.", 1, 9),
        _create_tf_challenge(u"En la huerta los almácigos retrasan la germinación de las semillas por tratarse de un microclima controlado.", 0, 9)
    ]
    return tf_challenges
    
def _create_mc_challenge(question, answers, level, image=None):
    """ Create a new mc_challenge (tuple) """
    return (question, answers, 0, level, image)
    
def _create_tf_challenge(question, correct_answer, level, image=None):
    """ Create a new tf_challenge (tuple) """
    return (question, [_("False"), _("True")], correct_answer, level, image)


class ChallengesCreator(GObject.Object):
    
    def __init__(self, container, rect, frame_rate, windows_controller, game_man, bg_color=(0, 0, 0)):
        GObject.Object.__init__(self)
        # Windows attributes
        self.container = container
        self.rect = rect
        self.frame_rate = frame_rate
        self.windows_controller = windows_controller
        self.bg_color = bg_color

        self.game_man = game_man
        
        # Multiple Choice and Master window
        self.mc_challenge = challenges.MultipleChoice(self.container, self.rect, self.frame_rate, self.windows_controller, self, "mc_challenge_window", self.bg_color)
        
        # True or False window
        self.tf_challenge = challenges.TrueOrFalse(self.container, self.rect, self.frame_rate, self.windows_controller, self, "tf_challenge_window", self.bg_color)
        
        # Cooking window
        #self.cooking_challenge = challenges.Cooking(self.container, self.rect, self.frame_rate, self.windows_controller, "cooking_challenge_window", self.bg_color)
        
        # Tuples of mc_challenges
        self.mc_challenges = None
        
        # Dict of true or false tuples
        self.tf_challenges = None
            
    def create_challenges(self):
        self.mc_challenges = get_mc_challenges()
        self.tf_challenges = get_tf_challenges()
    
    def get_challenge(self, kind):
        """
        Load and return a random "created" mc_challenge
        """
        if kind == "mc":
            
            bar = self.game_man.get_lowest_bar()
            
            challenges = self.mc_challenges[bar.id]
            
            r = random.randrange(0, len(challenges))
            c = challenges[r]
            
            # Set challenge attributes
            self.mc_challenge.set_question(c[0])
            self.mc_challenge.set_answers(c[1], c[2])
            
            # If challenge has an image
            if c[4]:
                self.mc_challenge.set_image(c[4])
                
            return self.mc_challenge
            
        elif kind == "tf":
            self.tf_challenge.kind = "normal"
            bar = self.game_man.get_lowest_bar()
            
            challenges = self.tf_challenges[bar.id]
            
            r = random.randrange(0, len(challenges))
            c = challenges[r]
            
            # Set challenge attributes
            self.tf_challenge.set_question(c[0])
            self.tf_challenge.set_answers(c[1], c[2])
            
            # If challenge has an image
            if c[4]:
                self.tf_challenge.set_image(c[4])
                
            return self.tf_challenge
                
        elif kind == "master":
            self.tf_challenge.kind = "master"
            
            l = random.randrange(0, 5)
            challenges = self.mc_challenges[self.mc_challenges.keys()[l]]
            
            r = random.randrange(0, len(challenges))
            c = challenges[r]
            
            # Set challenge attributes
            self.tf_challenge.set_question(c[0])
            self.tf_challenge.set_answers(c[1], c[2])
            
            # If challenge has an image
            if c[4]:
                self.tf_challenge.set_image(c[4])
                
            return self.tf_challenge
