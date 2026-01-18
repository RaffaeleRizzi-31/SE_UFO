import time

import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._current_year = None
        self._current_shape = None
        self._flag_grafo = False

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO
        anni = self._model.fill_dd_year()
        self._view.dd_year.options.clear()
        for a in sorted(anni):
            option = ft.dropdown.Option(text=str(a), data=a)
            self._view.dd_year.options.append(option)
        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        if self._current_year is None:
            self._view.show_alert("Selezionare prima un anno")
            return
        elif self._current_shape is None:
            self._view.show_alert("Selezionare prima un forma")
            return
        output_nodo_somma, n_nodi, n_archi = self._model.build_graph(self._current_shape, self._current_year)
        self._flag_grafo = True
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Numero di vertici: {n_nodi} Numero di archi: {n_archi}")
        )
        for id,somma in output_nodo_somma.items():
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Nodo {id}, somma pesi su archi = {somma}")
            )
        self._view.update()
    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        if not self._flag_grafo:
            self._view.show_alert("Creare prima il grafo")
            return
        best_path, best_distance = self._model.percorso()
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Peso cammino massimo: {best_distance}")
        )
        for arco, peso, distance_c in best_path:
            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f"{arco[0]} --> {arco[1]}: weight {peso} distance {distance_c}")
            )
        self._view.update()


    def get_selected_year(self,e):
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_2.controls.clear()
        self._flag_grafo = False
        self._current_shape = None
        self._view.dd_shape.key = f"dd_shape{time.time()}"
        self._view.dd_shape.options.clear()
        self._view.dd_shape.value = None
        selected_option = e.control.value
        if selected_option is None:
            self._current_year = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_year = found
        self.handle_fill_dd_shape(self._current_year)
        self._view.update()

    def handle_fill_dd_shape(self, anno):
        shape = self._model.fill_dd_shape(anno)
        self._view.dd_shape.options.clear()
        for s in shape:
            option = ft.dropdown.Option(text=str(s), data=s)
            self._view.dd_shape.options.append(option)
        self._view.update()

    def get_selected_shape(self,e):
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_2.controls.clear()
        self._flag_grafo = False
        selected_option = e.control.value
        if selected_option is None:
            self._current_shape = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_shape = found
        self._view.update()
