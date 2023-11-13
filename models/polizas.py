# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class polizas(models.Model):
    _name = 'itriplee.polizas'
    _rec_name = 'folio'
    _description = "Modulo de polizas"

    name = fields.Integer('ID de poliza', required=True)
    folio = fields.Integer('Folio', required=True)
    cliente = fields.Many2one('res.partner', 'Cliente', required=True)
    fecha_contratacion = fields.Date('Fecha de Contratación', required=True)
    tipo_poliza = fields.Selection([("con refacciones","Con Refacciones"),("sin refacciones","Sin Refacciones")], 'Tipo de Poliza', required=True)
    horario = fields.Selection([("24 / 7","24 / 7"),("Horario de Oficina","Horario de Oficina")], 'Horario Contratado', required=True)
    tiempo = fields.Selection([("1 año","1 año"),("2 años","2 años"),("3 años","3 años")], 'Duración de la Poliza')
    tiempo_int = fields.Integer("años de contratación")
    visitas_int = fields.Integer("Visitas contratadas por año")
    visitas_contratadas = fields.Selection([("1","1"),("2","2"),("3","3")], 'Visitas anuales contratadas')
    ubicacion = fields.Selection([("Local","Local"),("Foraneo","Foraneo")], 'Local o Foraneo')
    visitas = fields.One2many('itriplee.servicio', 'poliza_asociada', 'Visitas')
    equipos = fields.One2many('itriplee.equipos', 'poliza', 'Equipos')
    observaciones = fields.Text('Observaciones')

    def create_visita(self):
        cantidad = self.tiempo_int * self.visitas_int
        dias = cantidad * 365
        intervalo = dias / cantidad

        fecha_visita = self.fecha_contratacion + timedelta(days=intervalo)
        equipos_relacionados = []

        while cantidad > 0:
            # Crear un diccionario para cada equipo
            #equipo = {
             #   'name': 'Nombre del equipo',  # Ajusta este valor según tus necesidades
                # Otros campos del modelo 'itriplee.equipos' que desees asignar
            #}

            # Agregar la tupla (0, 0, equipo) a la lista de equipos_relacionados
            equipos_relacionados.append((6, 0, [self.equipos]))

            cantidad -= 1

            visita_programada = {
                'visita': fecha_visita,
                'cliente': self.cliente.id,
                'poliza_asociada': self.id,
                'equipos': equipos_relacionados
            }

            # Crear el registro en 'itriplee.servicio' con los equipos relacionados
            self.env['itriplee.servicio'].create(visita_programada)


    #Falta funcion para al momento de guardar se creen las visitas correspondientes
    #falta factura related