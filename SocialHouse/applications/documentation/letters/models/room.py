from django.core.exceptions import ValidationError
from django.db import models

from . import LetterBase


class RoomLetter(LetterBase):
    class Meta:
        verbose_name = "Заявление о смене комнаты"
        verbose_name_plural = "Заявления о сменах комнат"

    old_room = models.PositiveIntegerField(verbose_name="Номер текущей комнаты проживания", editable=False)
    old_floor = models.IntegerField(verbose_name="Текущий этаж проживания", editable=False)

    new_room = models.PositiveIntegerField(verbose_name="Номер новой комнаты проживания")
    new_floor = models.IntegerField(verbose_name="Номер новой комнаты проживания")

    reason = models.TextField(verbose_name="Причина переезда")

    def old_place(self):
        return f"{self.old_room} ({self.old_floor})"

    def new_place(self):
        return f"{self.new_room} ({self.new_floor})"

    old_place.short_description = "Из комнаты"
    new_place.short_description = "В комнату"

    # TODO signal !
    def clean(self):
        if self.new_room > self.department_info.department_rooms:
            raise ValidationError("Номер комнаты превышает количество комнат в отделении")
        if self.new_floor > self.department_info.department_floors:
            raise ValidationError("Этаж превышает количество этажей в отделении")

        self.old_room = self.serviced_person.room
        self.old_floor = self.serviced_person.floor
        print(f"Room for {self.serviced_person} changed from {self.serviced_person.room} ")
        self.serviced_person.room = self.new_room
        self.serviced_person.floor = self.new_floor
        self.serviced_person.save()
        print(f"(for {self.serviced_person})to {self.new_room}")

    def template_name(self):
        return "room.docx"
