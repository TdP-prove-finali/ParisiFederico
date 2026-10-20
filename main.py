import flet as ft

from UI.view import View
from model.model import Model
from UI.controller import Controller


def main(page: ft.Page):
    myModel = Model()
    myView = View(page)
    myController = Controller(myView, myModel)
    myView.set_controller(myController)
    myView.load_interface()


ft.app(target=main)